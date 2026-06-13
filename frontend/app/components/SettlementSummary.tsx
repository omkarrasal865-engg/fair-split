type Settlement = {
  from_person: string;
  to_person: string;
  amount: number;
};

type Props = {
  settlements: Settlement[];
};

export default function SettlementSummary({
  settlements,
}: Props) {
  return (
    <div className="h-full rounded-xl border bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-xl font-bold">
        Settlement Summary
      </h2>

      {settlements.length === 0 ? (
        <p className="text-slate-600">
          No settlements required.
        </p>
      ) : (
        <div className="space-y-3">
          {settlements.map(
            (settlement, index) => (
              <div
                key={index}
                className="rounded-lg bg-slate-50 p-3"
              >
                <span className="font-semibold">
                  {settlement.from_person}
                </span>

                {" → "}

                <span className="font-semibold">
                  {settlement.to_person}
                </span>

                <div className="mt-1 font-bold text-green-700">
                  ₹
                  {settlement.amount.toFixed(
                    2
                  )}
                </div>
              </div>
            )
          )}
        </div>
      )}
    </div>
  );
}