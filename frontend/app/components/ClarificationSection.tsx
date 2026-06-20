type Question = {
  id: string;
  type: string;
  item: string;
  remaining_quantity: number;
  remaining_amount: number;
  question: string;
};

type Props = {
  questions: Question[];
};

function formatAmount(value: number) {
  return value.toLocaleString("en-IN", {
    maximumFractionDigits: 2,
    minimumFractionDigits: 0,
  });
}

export default function ClarificationSection({
  questions,
}: Props) {
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

      {questions.map((question) => (
        <div
          key={question.id}
          className="rounded-2xl border border-[var(--border)] bg-[var(--surface)] p-4"
        >
          <h4 className="font-medium text-[var(--text)]">
            {question.question}
          </h4>

          <div className="mt-2 text-sm text-[var(--text-muted)]">
            <p>
              Remaining quantity: {question.remaining_quantity}
            </p>

            <p>
              Remaining amount: ₹
              {formatAmount(question.remaining_amount)}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}