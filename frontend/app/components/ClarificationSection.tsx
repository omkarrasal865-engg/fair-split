"use client";

import { useState } from "react";

import {
  submitClarification,
} from "../lib/api";

type Question = {
  id: string;
  type: string;
  item: string;
  remaining_quantity: number;
  remaining_amount: number;
  question: string;
  participants: string[];
};

type Props = {
  questions: Question[];

  sessionId: string;

  onCompleted: (result: any) => void;
};

function formatAmount(value: number) {
  return value.toLocaleString("en-IN", {
    maximumFractionDigits: 2,
    minimumFractionDigits: 0,
  });
}

export default function ClarificationSection({
  questions,
  sessionId,
  onCompleted,
}: Props) {
  const [answers, setAnswers] = useState<
    Record<string, Record<string, number>>
  >({});

  const [submitting, setSubmitting] =
    useState(false);

  const [error, setError] =
    useState("");

  function updateQuantity(
    questionId: string,
    participant: string,
    value: string
  ) {
    const quantity =
      value === ""
        ? 0
        : Number(value);

    setAnswers((prev) => ({
      ...prev,
      [questionId]: {
        ...(prev[questionId] || {}),
        [participant]: quantity,
      },
    }));
  }

  async function handleSubmit() {
    setError("");

    const invalidQuestion =
      questions.find((question) => {
        const totalAllocated =
          Object.values(
            answers[question.id] || {}
          ).reduce(
            (sum, value) =>
              sum + value,
            0
          );

        return (
          totalAllocated !==
          question.remaining_quantity
        );
      });

    if (invalidQuestion) {
      setError(
        "Please allocate all remaining quantities before submitting."
      );
      return;
    }

    try {
      setSubmitting(true);

      const payload =
        questions.map((question) => ({
          question_id:
            question.id,

          item:
            question.item,

          consumers:
            Object.entries(
              answers[
                question.id
              ] || {}
            )
              .filter(
                ([, quantity]) =>
                  quantity > 0
              )
              .map(
                ([
                  person,
                  quantity,
                ]) => ({
                  person,
                  quantity,
                })
              ),
        }));

      const result =
        await submitClarification(
          sessionId,
          payload
        );

      onCompleted(result);

    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to submit clarification."
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="space-y-4 animate-fade-up">
      <div className="rounded-2xl border border-yellow-500/30 bg-yellow-500/10 p-4">
        <h3 className="text-lg font-semibold text-yellow-300">
          Clarification Required
        </h3>

        <p className="mt-1 text-sm text-yellow-100/80">
          Some receipt items could not be allocated.
          Please answer the questions below.
        </p>
      </div>

      {questions.map((question) => {
        const totalAllocated =
          Object.values(
            answers[question.id] || {}
          ).reduce(
            (sum, value) =>
              sum + value,
            0
          );

        const isValid =
          totalAllocated ===
          question.remaining_quantity;

        return (
          <div
            key={question.id}
            className="rounded-2xl border border-[var(--border)] bg-[var(--surface)] p-4"
          >
            <h4 className="font-medium text-[var(--text)]">
              {question.question}
            </h4>

            <div className="mt-2 text-sm text-[var(--text-muted)]">
              <p>
                Remaining quantity:{" "}
                {question.remaining_quantity}
              </p>

              <p>
                Remaining amount: ₹
                {formatAmount(
                  question.remaining_amount
                )}
              </p>
            </div>

            <div className="mt-4 space-y-3">
              {question.participants.map(
                (participant) => (
                  <div
                    key={participant}
                    className="flex items-center justify-between gap-4"
                  >
                    <span className="text-sm text-[var(--text)]">
                      {participant}
                    </span>

                    <input
                      type="number"
                      min="0"
                      step="1"
                      placeholder="0"
                      value={
                        answers[
                          question.id
                        ]?.[
                          participant
                        ] ?? ""
                      }
                      onChange={(e) =>
                        updateQuantity(
                          question.id,
                          participant,
                          e.target.value
                        )
                      }
                      className="w-24 rounded-xl border border-[var(--border)] bg-[var(--surface-2)] px-3 py-2 text-sm text-[var(--text)] outline-none"
                    />
                  </div>
                )
              )}
            </div>

            <div className="mt-4 rounded-xl bg-[var(--surface-2)] p-3 text-sm">
              <div className="flex items-center justify-between">
                <span>
                  Allocated:
                </span>

                <span>
                  {totalAllocated} /{" "}
                  {
                    question.remaining_quantity
                  }
                </span>
              </div>

              <div className="mt-2">
                {isValid ? (
                  <span className="text-green-400">
                    ✓ Quantity matches
                  </span>
                ) : (
                  <span className="text-yellow-400">
                    Remaining quantity must total{" "}
                    {
                      question.remaining_quantity
                    }
                  </span>
                )}
              </div>
            </div>
          </div>
        );
      })}

      {error && (
        <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-300">
          {error}
        </div>
      )}

      <button
        type="button"
        onClick={handleSubmit}
        disabled={submitting}
        className="w-full rounded-2xl bg-[var(--accent)] px-4 py-3 text-sm font-semibold text-[#06231a]"
      >
        {submitting
          ? "Submitting..."
          : "Submit Clarifications"}
      </button>
    </div>
  );
}