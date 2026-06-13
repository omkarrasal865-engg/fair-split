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

export default function BillSummary({
  grandTotal,
  paidBy,
  reconciliation,
  flags,
  assumptions,
}: Props) {
  return (
    <div className="h-full rounded-xl border bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-xl font-bold">
        Bill Summary
      </h2>

      <div className="space-y-3">
        <p>
          <strong>Grand Total:</strong>{" "}
          ₹{grandTotal}
        </p>

        <p>
          <strong>Paid By:</strong>{" "}
          {paidBy}
        </p>

        <p>
          <strong>Status:</strong>{" "}
          {reconciliation.matches_bill
            ? "✅ Matches Bill"
            : "❌ Mismatch"}
        </p>

        <p>
          <strong>Difference:</strong>{" "}
          ₹{reconciliation.difference}
        </p>
      </div>

      <div className="mt-6">
        <h3 className="font-semibold">
          Flags
        </h3>

        {flags.length === 0 ? (
          <p className="text-slate-600">
            None
          </p>
        ) : (
          <ul className="mt-2 space-y-1">
            {flags.map((flag, index) => (
              <li key={index}>
                • {flag}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="mt-6">
        <h3 className="font-semibold">
          Assumptions
        </h3>

        {assumptions.length === 0 ? (
          <p className="text-slate-600">
            None
          </p>
        ) : (
          <ul className="mt-2 space-y-1">
            {assumptions.map(
              (
                assumption,
                index
              ) => (
                <li key={index}>
                  • {assumption}
                </li>
              )
            )}
          </ul>
        )}
      </div>
    </div>
  );
}