type Person = {
  name: string;
  items: string[];
  total: number;
};

type Props = {
  people: Person[];
};

export default function ResultsSection({
  people,
}: Props) {
  return (
    <div className="mt-8">
      <h2 className="mb-4 text-2xl font-bold">
        Per Person
      </h2>

      <div className="grid gap-4 md:grid-cols-2">
        {people.map((person) => (
          <div
            key={person.name}
            className="rounded-xl border bg-white p-5 shadow-sm"
          >
            <div className="flex items-center justify-between">
              <h3 className="text-xl font-semibold">
                {person.name}
              </h3>

              <span className="text-lg font-bold text-blue-600">
                ₹{person.total.toFixed(2)}
              </span>
            </div>

            <div className="mt-4">
              <p className="mb-2 font-medium">
                Items
              </p>

              <ul className="space-y-1 text-sm text-slate-700">
                {person.items.map((item, index) => (
                  <li key={index}>
                    • {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}