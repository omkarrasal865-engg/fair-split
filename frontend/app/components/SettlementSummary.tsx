type Settlement = {
  from_person: string;
  to_person: string;
  amount: number;
};

type Props = {
  settlements: Settlement[];
};

function formatAmount(value: number) {
  return value.toLocaleString("en-IN", {
    maximumFractionDigits: 2,
    minimumFractionDigits: 0,
  });
}

export default function SettlementSummary({ settlements }: Props) {
  return (
    <div className="animate-fade-up">
      <div className="mb-3 px-1">
        <h3 className="text-sm font-semibold text-[var(--text)]">
          Settle up
        </h3>
        <p className="text-xs text-[var(--text-muted)]">
          {settlements.length === 0
            ? "Everyone's even — nothing to settle."
            : "These are the payments needed to even things out."}
        </p>
      </div>

      {settlements.length === 0 ? (
        <div className="flex items-center gap-3 rounded-2xl border border-[var(--border)] bg-[var(--surface)] px-4 py-5">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[var(--accent-dim)] text-lg">
            ✅
          </div>
          <p className="text-sm text-[var(--text)]">
            No settlements required.
          </p>
        </div>
      ) : (
        <div className="space-y-2.5">
          {settlements.map((settlement, index) => (
            <div
              key={index}
              className="flex items-center justify-between gap-3 rounded-2xl border border-[var(--border)] bg-gradient-to-br from-[var(--surface)] to-[var(--surface-2)] px-4 py-4"
            >
              <div className="flex items-center gap-2.5 text-sm font-medium text-[var(--text)]">
                <span className="rounded-full bg-[var(--surface-2)] px-2.5 py-1">
                  {settlement.from_person}
                </span>
                <span className="text-[var(--text-muted)]" aria-hidden>
                  →
                </span>
                <span className="rounded-full bg-[var(--surface-2)] px-2.5 py-1">
                  {settlement.to_person}
                </span>
              </div>

              <div className="num text-lg font-bold text-[var(--accent)]">
                ₹{formatAmount(settlement.amount)}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
