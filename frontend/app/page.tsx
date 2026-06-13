import ReceiptUploadForm from "./components/ReceiptUploadForm";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-100 px-4 py-10">
      <div className="mx-auto max-w-4xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-slate-900">
            Fair Split
          </h1>

          <p className="mt-3 text-slate-600">
            AI-Powered Restaurant Bill Splitting
          </p>
        </div>

        <ReceiptUploadForm />
      </div>
    </main>
  );
}