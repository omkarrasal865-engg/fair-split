import ReceiptUploadForm from "./components/ReceiptUploadForm";

export default function Home() {
  return (
    <main className="min-h-screen px-4 py-10 sm:py-14">
      <div className="mx-auto w-full max-w-xl">
        <div className="mb-8 flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[var(--accent-dim)] text-xl">
            🧾
          </div>
          <div>
            <h1 className="text-2xl font-semibold tracking-tight text-[var(--text)]">
              Fair Split
            </h1>
            <p className="text-sm text-[var(--text-muted)]">
              AI-powered restaurant bill splitting
            </p>
          </div>
        </div>

        <ReceiptUploadForm />
      </div>
    </main>
  );
}
