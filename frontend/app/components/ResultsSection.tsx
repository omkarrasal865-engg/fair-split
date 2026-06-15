"use client";

import { useState } from "react";

type Person = {
  name: string;
  items: string[];
  subtotal: number;
  tax_share: number;
  service_share: number;
  discount_share: number;
  total: number;
};

type Props = {
  people: Person[];
};

function formatAmount(value: number) {
  return value.toLocaleString("en-IN", {
    maximumFractionDigits: 2,
    minimumFractionDigits: 0,
  });
}

export default function ResultsSection({ people }: Props) {
  const [openName, setOpenName] = useState<string | null>(
    people[0]?.name ?? null
  );

  return (
    <div className="animate-fade-up">
      <div className="mb-3 flex items-center justify-between px-1">
        <h3 className="text-sm font-semibold text-[var(--text)]">
          Per person
        </h3>
        <span className="text-xs text-[var(--text-muted)]">
          {people.length} {people.length === 1 ? "person" : "people"}
        </span>
      </div>

      <div className="space-y-2.5">
        {people.map((person) => {
          const isOpen = openName === person.name;

          return (
            <div
              key={person.name}
              className="overflow-hidden rounded-2xl border border-[var(--border)] bg-[var(--surface)] transition-colors"
            >
              <button
                type="button"
                onClick={() => setOpenName(isOpen ? null : person.name)}
                className="flex w-full items-center justify-between gap-3 px-4 py-3.5 text-left"
                aria-expanded={isOpen}
              >
                <div className="flex items-center gap-3">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[var(--surface-2)] text-sm font-semibold text-[var(--text)]">
                    {person.name.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <p className="text-sm font-medium text-[var(--text)]">
                      {person.name}
                    </p>
                    <p className="text-xs text-[var(--text-muted)]">
                      {person.items.length}{" "}
                      {person.items.length === 1 ? "item" : "items"}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span className="num text-base font-semibold text-[var(--text)]">
                    ₹{formatAmount(person.total)}
                  </span>
                  <span
                    className={`text-[var(--text-muted)] transition-transform ${
                      isOpen ? "rotate-180" : ""
                    }`}
                    aria-hidden
                  >
                    ▾
                  </span>
                </div>
              </button>

              {isOpen && (
                <div className="border-t border-[var(--border)] px-4 py-3.5 animate-fade-up">
                  <ul className="space-y-1.5 text-sm text-[var(--text-muted)]">
                    {person.items.map((item, index) => (
                      <li key={index} className="flex items-start gap-2">
                        <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-[var(--text-muted)]" />
                        <span className="text-[var(--text)]">{item}</span>
                      </li>
                    ))}
                  </ul>

                  <div className="mt-3 space-y-1.5 border-t border-[var(--border)] pt-3 text-sm">
                    <div className="flex justify-between text-[var(--text-muted)]">
                      <span>Subtotal</span>
                      <span className="num">₹{formatAmount(person.subtotal)}</span>
                    </div>
                    <div className="flex justify-between text-[var(--text-muted)]">
                      <span>Tax</span>
                      <span className="num">₹{formatAmount(person.tax_share)}</span>
                    </div>
                    <div className="flex justify-between text-[var(--text-muted)]">
                      <span>Service charge</span>
                      <span className="num">₹{formatAmount(person.service_share)}</span>
                    </div>
                    {person.discount_share !== 0 && (
                      <div className="flex justify-between text-[var(--accent)]">
                        <span>Discount</span>
                        <span className="num">₹{formatAmount(person.discount_share)}</span>
                      </div>
                    )}
                    <div className="flex justify-between border-t border-[var(--border)] pt-1.5 font-semibold text-[var(--text)]">
                      <span>Total</span>
                      <span className="num">₹{formatAmount(person.total)}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
