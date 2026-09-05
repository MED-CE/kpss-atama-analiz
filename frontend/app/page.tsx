import Dashboard from "@/components/Dashboard";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-8 lg:p-24 bg-gray-50">
      <div className="z-10 max-w-7xl w-full items-center justify-between font-sans mb-12">
        <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 mb-4">
          KPSS Merkezi Atama Analiz Platformu
        </h1>
        <p className="text-lg text-gray-600 max-w-3xl">
          2010'dan günümüze ÖSYM KPSS merkezi atama verilerini (kontenjan, yerleşen aday, taban-tavan puanlar) analiz edin.
        </p>
      </div>
      
      <div className="w-full max-w-7xl">
        <Dashboard />
      </div>
    </main>
  );
}
