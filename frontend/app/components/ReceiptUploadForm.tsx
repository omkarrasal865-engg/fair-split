"use client";

import { useState } from "react";
import { splitBill } from "../lib/api";

import ResultsSection from "./ResultsSection";
import SettlementSummary from "./SettlementSummary";
import BillSummary from "./BillSummary";

import { SplitBillResponse } from "../types/api";

export default function ReceiptUploadForm() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [fileInputKey, setFileInputKey] = useState(0);

  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [response, setResponse] =
    useState<SplitBillResponse | null>(null);

  async function handleSubmit(
    e: React.FormEvent<HTMLFormElement>
  ) {
    e.preventDefault();

    setError("");
    setResponse(null);

    if (!file) {
      setError("Please upload a receipt image.");
      return;
    }

    if (!description.trim()) {
      setError("Please enter a description.");
      return;
    }

    try {
      setLoading(true);

      const result = await splitBill(
        file,
        description
      );

      setResponse(result);
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

  function resetForm() {
    setFile(null);
    setPreviewUrl(null);
    setDescription("");
    setResponse(null);
    setError("");

    setFileInputKey((prev) => prev + 1);
  }

  return (
    <div className="w-full max-w-5xl rounded-2xl bg-white p-6 shadow-lg">
      <form
        onSubmit={handleSubmit}
        className="space-y-6"
      >
        <div>
          <label className="mb-2 block text-sm font-medium text-gray-700">
            Upload Receipt
          </label>

          <input
            key={fileInputKey}
            type="file"
            accept="image/*"
            disabled={loading}
            onChange={(e) => {
              const selectedFile =
                e.target.files?.[0] || null;

              setFile(selectedFile);

              if (selectedFile) {
                setPreviewUrl(
                  URL.createObjectURL(
                    selectedFile
                  )
                );
              } else {
                setPreviewUrl(null);
              }
            }}
            className="block w-full rounded-lg border border-gray-300 p-3 disabled:bg-gray-100"
          />

          {previewUrl && (
            <div className="mt-4">
              <p className="mb-2 text-sm font-medium text-gray-700">
                Receipt Preview
              </p>

              <div className="overflow-hidden rounded-lg border border-gray-300">
                <img
                  src={previewUrl}
                  alt="Receipt Preview"
                  className="max-h-96 w-full object-contain bg-gray-50"
                />
              </div>

              {file && (
                <p className="mt-2 text-sm text-gray-500">
                  {file.name}
                </p>
              )}
            </div>
          )}
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-gray-700">
            Description
          </label>

          <textarea
            rows={8}
            value={description}
            disabled={loading}
            onChange={(e) =>
              setDescription(e.target.value)
            }
            placeholder="Describe who consumed what..."
            className="w-full rounded-lg border border-gray-300 p-4 outline-none focus:border-blue-500 disabled:bg-gray-100"
          />
        </div>

        {error && (
          <div className="rounded-lg border border-red-300 bg-red-50 p-3 text-red-700">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
        >
          {loading
            ? "Calculating..."
            : "Calculate Split"}
        </button>
      </form>

      {loading && (
        <div className="mt-8 rounded-2xl border border-blue-200 bg-blue-50 p-6">
          <div className="flex items-center gap-4">
            <div className="h-10 w-10 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600" />

            <div>
              <h3 className="font-semibold text-blue-900">
                Processing Receipt
              </h3>

              <p className="text-sm text-blue-700">
                This may take 10–20 seconds
              </p>
            </div>
          </div>

          <div className="mt-6 space-y-3">
            <div className="rounded-lg bg-white p-3">
              📤 Uploading receipt image
            </div>

            <div className="rounded-lg bg-white p-3">
              🤖 Extracting receipt data with AI
            </div>

            <div className="rounded-lg bg-white p-3">
              ⚖️ Calculating fair split
            </div>

            <div className="rounded-lg bg-white p-3">
              💸 Generating settlements
            </div>
          </div>
        </div>
      )}

      {response?.data && (
        <>
          <div className="mt-8 flex justify-end">
            <button
              type="button"
              onClick={resetForm}
              className="rounded-lg bg-slate-700 px-4 py-2 text-white transition hover:bg-slate-800"
            >
              Analyze Another Receipt
            </button>
          </div>

          <ResultsSection
            people={response.data.per_person}
          />

          <div className="mt-8 grid gap-6 md:grid-cols-2">
            <SettlementSummary
              settlements={
                response.data.settle_up
              }
            />

            <BillSummary
              grandTotal={
                response.data.grand_total
              }
              paidBy={
                response.data.paid_by
              }
              reconciliation={
                response.data.reconciliation
              }
              flags={response.data.flags}
              assumptions={
                response.data.assumptions
              }
            />
          </div>
        </>
      )}
    </div>
  );
}