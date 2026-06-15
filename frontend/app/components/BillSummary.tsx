type Props = {
  grandTotal: number;
  paidBy: string;
  reconciliation: {
    matches_bill: boolean;
    difference: number;
  };
  flags: string[];
  assumptions: string[];
};

function formatAmount(value: number) {
  return value.toLocaleString("en-IN", {
    maximumFractionDigits: 2,
    minimumFractionDigits: 0,
  });
}

export default function BillSummary({
  grandTotal,
  paidBy,
  reconciliation,
  flags,
  assumptions,
}: Props) {
  return (
    <div className="space-y-2.5 animate-fade-up">
      {/* Bill summary card */}
      <div className="rounded-2xl border border-[var(--border)] bg-[var(--surface)] p-4">
        <h3 className="mb-3 text-sm font-semibold text-[var(--text)]">
          Bill summary
        </h3>

        <div className="space-y-2 text-sm">
          <div className="flex items-center justify-between">
            <span className="text-[var(--text-muted)]">Grand total</span>
            <span className="num font-semibold text-[var(--text)]">
              ₹{formatAmount(grandTotal)}
            </span>
          </div>

          <div className="flex items-center justify-between">
            <span className="text-[var(--text-muted)]">Paid by</span>
            <span className="font-medium text-[var(--text)]">{paidBy}</span>
          </div>

          <div className="flex items-center justify-between border-t border-[var(--border)] pt-2">
            <span className="text-[var(--text-muted)]">Reconciliation</span>
            {reconciliation.matches_bill ? (
              <span className="inline-flex items-center gap-1.5 rounded-full bg-[var(--accent-dim)] px-2.5 py-1 text-xs font-medium text-[var(--accent)]">
                <span aria-hidden>✓</span> Matches bill
              </span>
            ) : (
              <span className="inline-flex items-center gap-1.5 rounded-full bg-[var(--danger-dim)] px-2.5 py-1 text-xs font-medium text-[var(--danger)]">
                <span aria-hidden>⚠</span> Off by ₹
                {formatAmount(Math.abs(reconciliation.difference))}
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Flags */}
      {flags.length > 0 && (
        <div className="rounded-2xl border border-[var(--warn)]/25 bg-[var(--warn-dim)] p-4">
          <h3 className="mb-2 flex items-center gap-1.5 text-sm font-semibold text-[var(--warn)]">
            <span aria-hidden>⚠️</span> Flags
          </h3>
          <ul className="space-y-1.5 text-sm text-[var(--text)]">
            {flags.map((flag, index) => (
              <li key={index} className="flex items-start gap-2">
                <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-[var(--warn)]" />
                <span>{flag}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Assumptions */}
      {assumptions.length > 0 && (
        <div className="rounded-2xl border border-[var(--border)] bg-[var(--surface)] p-4">
          <h3 className="mb-2 flex items-center gap-1.5 text-sm font-semibold text-[var(--text)]">
            <span aria-hidden>💡</span> Assumptions
          </h3>
          <ul className="space-y-1.5 text-sm text-[var(--text-muted)]">
            {assumptions.map((assumption, index) => (
              <li key={index} className="flex items-start gap-2">
                <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-[var(--text-muted)]" />
                <span>{assumption}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
