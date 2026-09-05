import Dashboard from "@/components/Dashboard";
import FilterTable from "@/components/FilterTable";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-4 md:p-8 lg:p-16 bg-slate-50">
      <div className="z-10 w-full items-center justify-between font-sans mb-8">
        <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-gray-900 mb-2">
          KPSS Merkezi Atama Analizi
        </h1>
        <p className="text-base text-gray-500 max-w-3xl">
          2010'dan günümüze ÖSYM atama verilerini inceleyin.
        </p>
      </div>
      
      <div className="w-full">
        <Dashboard />
        <FilterTable />
      </div>
    </main>
  );
}
