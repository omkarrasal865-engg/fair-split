"use client";

import { useState, useRef, useEffect } from "react";
import {
  splitBill,
} from "../lib/api";

import ResultsSection from "./ResultsSection";
import SettlementSummary from "./SettlementSummary";
import BillSummary from "./BillSummary";
import ClarificationSection from "./ClarificationSection";

import { SplitBillResponse } from "../types/api";

const PROCESSING_STEPS = [
  { emoji: "📤", label: "Uploading receipt image" },
  { emoji: "🤖", label: "Extracting receipt data with AI" },
  { emoji: "⚖️", label: "Calculating fair split" },
  { emoji: "💸", label: "Generating settlements" },
];

export default function ReceiptUploadForm() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [fileInputKey, setFileInputKey] = useState(0);

  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [response, setResponse] = useState<SplitBillResponse | null>(null);

  const [sessionId, setSessionId] =
  useState<string | null>(null);

  const dropRef = useRef<HTMLLabelElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isListening, setIsListening] =
  useState(false);

const recognitionRef = useRef<any>(null);

useEffect(() => {
  if (typeof window === "undefined") return;

  const SpeechRecognition =
    (window as any).SpeechRecognition ||
    (window as any).webkitSpeechRecognition;

  if (!SpeechRecognition) {
    return;
  }

  const recognition =
    new SpeechRecognition();

  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = "en-IN";

  recognition.onresult = (
    event: any
  ) => {
    let transcript = "";

    for (
      let i = event.resultIndex;
      i < event.results.length;
      i++
    ) {
      transcript +=
        event.results[i][0].transcript + " ";
    }

    if (transcript.trim()) {
      setDescription((prev) =>
        prev
          ? prev + " " + transcript.trim()
          : transcript.trim()
      );
    }
  };

  recognition.onend = () => {
    setIsListening(false);
  };

  recognitionRef.current =
    recognition;

  return () => {
    recognition.stop();
  };
}, []);

  function applyFile(selectedFile: File | null) {
    setFile(selectedFile);

    if (selectedFile) {
      setPreviewUrl(URL.createObjectURL(selectedFile));
    } else {
      setPreviewUrl(null);
    }
  }

  async function handleSubmit(
  e: React.FormEvent<HTMLFormElement>
) {
  e.preventDefault();

  setError("");
  setResponse(null);

  if (!file) {
    setError(
      "Please upload a receipt image."
    );
    return;
  }

  if (!description.trim()) {
    setError(
      "Please enter a description."
    );
    return;
  }

  try {
    setLoading(true);

    const result = await splitBill(
      file,
      description
    );

    setResponse(result);

    if (
      result.data.status ===
      "needs_clarification"
    ) {
      setSessionId(
        result.data.session_id || null
      );
    }

  } catch (err) {
    setError(
      err instanceof Error
        ? err.message
        : "Something went wrong."
    );
  } finally {
    setLoading(false);
  }
}

  function startListening() {
  if (
    !recognitionRef.current
  ) {
    alert(
      "Voice recognition is not supported in this browser."
    );
    return;
  }

  setIsListening(true);

  recognitionRef.current.start();
}

function stopListening() {
  recognitionRef.current?.stop();

  setIsListening(false);
}

  function resetForm() {
    setFile(null);
    setPreviewUrl(null);
    setDescription("");
    setResponse(null);
    setError("");

    setFileInputKey((prev) => prev + 1);
  }

  const showForm = !response;

  return (
    <div className="w-full">
      {showForm && (
        <form
          onSubmit={handleSubmit}
          className="space-y-5 rounded-3xl border border-[var(--border)] bg-[var(--surface)] p-5 sm:p-6"
        >
          {/* Upload Receipt */}
          <div>
            <label className="mb-2 block text-sm font-medium text-[var(--text)]">
              Receipt
            </label>

            <label
              ref={dropRef}
              htmlFor="receipt-file"
              onDragOver={(e) => {
                e.preventDefault();
                if (!loading) setIsDragging(true);
              }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={(e) => {
                e.preventDefault();
                setIsDragging(false);
                if (loading) return;
                const dropped = e.dataTransfer.files?.[0];
                if (dropped) applyFile(dropped);
              }}
              className={`group relative flex cursor-pointer flex-col items-center justify-center gap-2 rounded-2xl border-2 border-dashed px-4 py-8 text-center transition-colors
                ${
                  isDragging
                    ? "border-[var(--accent)] bg-[var(--accent-dim)]"
                    : "border-[var(--border)] bg-[var(--surface-2)] hover:border-[var(--accent)]/50"
                }
                ${loading ? "cursor-not-allowed opacity-60" : ""}
              `}
            >
              <input
                key={fileInputKey}
                id="receipt-file"
                type="file"
                accept="image/*"
                disabled={loading}
                onChange={(e) => {
                  const selectedFile = e.target.files?.[0] || null;
                  applyFile(selectedFile);
                }}
                className="sr-only"
              />

              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[var(--surface)] text-lg">
                📷
              </div>

              <div>
                <p className="text-sm font-medium text-[var(--text)]">
                  {file ? "Choose a different photo" : "Upload a photo of the bill"}
                </p>
                <p className="mt-0.5 text-xs text-[var(--text-muted)]">
                  Tap to browse, or drag an image here
                </p>
              </div>
            </label>

            {previewUrl && (
              <div className="mt-4 animate-fade-up">
                <p className="mb-2 text-xs font-medium uppercase tracking-wide text-[var(--text-muted)]">
                  Receipt preview
                </p>

                <div className="overflow-hidden rounded-2xl border border-[var(--border)] bg-[var(--surface-2)]">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={previewUrl}
                    alt="Receipt Preview"
                    className="max-h-80 w-full object-contain"
                  />
                </div>

                {file && (
                  <div className="mt-2 flex items-center justify-between gap-2 text-xs text-[var(--text-muted)]">
                    <span className="truncate">{file.name}</span>
                    <button
                      type="button"
                      onClick={() => applyFile(null)}
                      disabled={loading}
                      className="shrink-0 rounded-full border border-[var(--border)] px-2.5 py-1 text-[var(--text-muted)] transition hover:border-[var(--danger)] hover:text-[var(--danger)] disabled:opacity-50"
                    >
                      Remove
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Description */}
          <div>
            <div className="mb-2 flex items-center justify-between">
  <label className="text-sm font-medium text-[var(--text)]">
    Who had what?
  </label>

  <button
    type="button"
    disabled={loading}
    onClick={
      isListening
        ? stopListening
        : startListening
    }
    className={`rounded-full px-3 py-1 text-xs font-medium transition ${
      isListening
        ? "bg-red-500 text-white"
        : "bg-[var(--surface-2)] text-[var(--text)]"
    }`}
  >
    {isListening
      ? "🔴 Listening..."
      : "🎤 Speak"}
  </button>
</div>

            <textarea
              rows={6}
              value={description}
              disabled={loading}
              onChange={(e) => setDescription(e.target.value)}
              placeholder={`e.g. "Aman skipped drinks. Priya and I shared the pasta. Everything else was common to all of us. Priya paid."`}
              className="w-full resize-none rounded-2xl border border-[var(--border)] bg-[var(--surface-2)] p-4 text-sm text-[var(--text)] outline-none placeholder:text-[var(--text-muted)] transition-colors focus:border-[var(--accent)] disabled:opacity-60"
            />
          </div>

          {error && (
            <div className="flex items-start gap-2 rounded-2xl border border-[var(--danger)]/30 bg-[var(--danger-dim)] p-3 text-sm text-[var(--danger)]">
              <span aria-hidden>⚠️</span>
              <span>{error}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="flex w-full items-center justify-center gap-2 rounded-2xl bg-[var(--accent)] px-4 py-3.5 text-sm font-semibold text-[#06231a] transition active:scale-[0.99] hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? (
              <>
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-[#06231a]/30 border-t-[#06231a]" />
                Calculating split…
              </>
            ) : (
              "Calculate split"
            )}
          </button>
        </form>
      )}

      {/* Processing state */}
      {loading && (
        <div className="mt-5 animate-fade-up rounded-3xl border border-[var(--border)] bg-[var(--surface)] p-5 sm:p-6">
          <div className="flex items-center gap-4">
            <div className="relative h-11 w-11 shrink-0">
              <div className="absolute inset-0 rounded-full border-2 border-[var(--border)]" />
              <div className="absolute inset-0 animate-spin rounded-full border-2 border-transparent border-t-[var(--accent)]" />
            </div>

            <div>
              <h3 className="text-sm font-semibold text-[var(--text)]">
                Processing your receipt
              </h3>
              <p className="text-xs text-[var(--text-muted)]">
                This usually takes 10–20 seconds
              </p>
            </div>
          </div>

          <div className="mt-5 space-y-2">
            {PROCESSING_STEPS.map((step, i) => (
              <div
                key={step.label}
                className="flex items-center gap-3 rounded-xl bg-[var(--surface-2)] px-3 py-2.5 text-sm text-[var(--text)] animate-fade-up"
                style={{ animationDelay: `${i * 120}ms` }}
              >
                <span className="text-base" aria-hidden>
                  {step.emoji}
                </span>
                <span>{step.label}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Results */}
      {response?.data && (
        <div className="space-y-5">
          <div className="flex items-center justify-between animate-fade-up">
            <div>
              <p className="text-xs uppercase tracking-wide text-[var(--text-muted)]">
                Processing complete
              </p>

              <h2 className="text-lg font-semibold text-[var(--text)]">
                Fair Split Result
              </h2>
            </div>

            <button
              type="button"
              onClick={resetForm}
              className="rounded-full border border-[var(--border)] bg-[var(--surface)] px-4 py-2 text-sm font-medium text-[var(--text)] transition hover:border-[var(--accent)]/50"
            >
              New receipt
            </button>
          </div>

          {response.data.status === "needs_clarification" && (
  <ClarificationSection
    questions={
      response.data.clarification?.questions || []
    }
    sessionId={sessionId || ""}
    onCompleted={(result) => {
      setResponse(result);
    }}
  />
)}

          {response.data.status === "completed" && response.data.data && (
            <>
              <SettlementSummary
                settlements={response.data.data.settle_up}
              />

              <ResultsSection
                people={response.data.data.per_person}
              />

              <BillSummary
               grandTotal={response.data.data.grand_total}
               paidBy={response.data.data.paid_by}
               merchantName={
                 response.data.data.merchant_name
              }
               expenseCategory={
                 response.data.data.expense_category
               }
               insights={
                 response.data.data.insights
              }
               reconciliation={
                 response.data.data.reconciliation
              }
               flags={
                 response.data.data.flags
              }
              assumptions={
                response.data.data.assumptions
              }
            />
            </>
          )}
        </div>
      )}
    </div>
  );
}