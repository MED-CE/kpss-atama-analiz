"use client"

import React, { useState } from 'react';
import { Card, CardContent } from './ui/card';
import { Search, Filter, ChevronDown, Heart, ListFilter } from 'lucide-react';

// Mock Data matching the screenshot structure
const MOCK_DATA = [
  { id: 1, institution: "İSTANBUL İL SAĞLIK MÜDÜRLÜĞÜ", ministry: "SAĞLIK BAKANLIĞI", program: "TEKNİSYEN (BİLİŞİM)", level: "Ortaöğretim", city: "İSTANBUL", period: "2024/5", quota: 1, placed: 1, minScore: 84.88, maxScore: 84.88 },
  { id: 2, institution: "T.C. SAĞLIK BAKANLIĞI İSTANBUL KANUNİ SULTAN SÜLEYMAN...", ministry: "SAĞLIK BAKANLIĞI", program: "TEKNİSYEN (BİLİŞİM)", level: "Ortaöğretim", city: "İSTANBUL", period: "2024/4", quota: 4, placed: 4, minScore: 84.43, maxScore: 88.23 },
  { id: 3, institution: "T.C. SAĞLIK BAKANLIĞI İSTANBUL SÜREYYAPAŞA GÖĞÜS...", ministry: "SAĞLIK BAKANLIĞI", program: "TEKNİSYEN (BİLİŞİM)", level: "Ortaöğretim", city: "İSTANBUL", period: "2023/5", quota: 1, placed: 1, minScore: 83.37, maxScore: 83.37 },
  { id: 4, institution: "T.C. SAĞLIK BAKANLIĞI İSTANBUL ZEYNEP KAMİL KADIN...", ministry: "SAĞLIK BAKANLIĞI", program: "TEKNİSYEN (BİLİŞİM)", level: "Ortaöğretim", city: "İSTANBUL", period: "2023/5", quota: 1, placed: 1, minScore: 82.50, maxScore: 82.50 },
];

export default function FilterTable() {
  const [searchTerm, setSearchTerm] = useState("");

  return (
    <div className="w-full space-y-6 mt-12">
      {/* Filter Section */}
      <Card className="border-gray-200 shadow-sm">
        <CardContent className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Branş/Bölüm</label>
              <div className="relative">
                <select className="w-full appearance-none rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
                  <option>TEKNİSYEN (BİLİŞİM)</option>
                  <option>HEMŞİRE</option>
                  <option>MÜHENDİS</option>
                </select>
                <ChevronDown className="absolute right-3 top-2.5 h-4 w-4 text-gray-500 pointer-events-none" />
              </div>
            </div>

            <div className="space-y-2 lg:col-span-1">
              <label className="text-sm font-medium text-gray-700">Arama</label>
              <div className="relative">
                <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
                <input 
                  type="text" 
                  placeholder="Kurum veya bölüm ara..." 
                  className="w-full rounded-md border border-gray-300 bg-white pl-9 pr-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Şehir</label>
              <div className="relative">
                <select className="w-full appearance-none rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
                  <option>İSTANBUL</option>
                  <option>ANKARA</option>
                  <option>İZMİR</option>
                  <option>Tümü</option>
                </select>
                <ChevronDown className="absolute right-3 top-2.5 h-4 w-4 text-gray-500 pointer-events-none" />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Kurum / Bakanlık</label>
              <div className="relative">
                <select className="w-full appearance-none rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
                  <option>Bakanlık seçiniz</option>
                  <option>SAĞLIK BAKANLIĞI</option>
                  <option>TARIM BAKANLIĞI</option>
                </select>
                <ChevronDown className="absolute right-3 top-2.5 h-4 w-4 text-gray-500 pointer-events-none" />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Nitelik Kodu</label>
              <div className="relative">
                <select className="w-full appearance-none rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
                  <option>Nitelik kodu seçiniz</option>
                  <option>2011</option>
                  <option>4001</option>
                </select>
                <ChevronDown className="absolute right-3 top-2.5 h-4 w-4 text-gray-500 pointer-events-none" />
              </div>
            </div>
            
          </div>

          <div className="flex justify-between items-end mt-4">
            <div className="space-y-2 w-48">
              <label className="text-sm font-medium text-gray-700">Yıl</label>
              <div className="relative">
                <select className="w-full appearance-none rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
                  <option>Tümü</option>
                  <option>2024</option>
                  <option>2023</option>
                </select>
                <ChevronDown className="absolute right-3 top-2.5 h-4 w-4 text-gray-500 pointer-events-none" />
              </div>
            </div>

            <div className="flex space-x-3">
              <button className="flex items-center px-4 py-2 text-sm font-medium text-blue-700 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100 transition-colors">
                <ListFilter className="w-4 h-4 mr-2" />
                Detaylı Filtreler
              </button>
              <button className="px-4 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">
                Filtreleri Temizle
              </button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Table Section */}
      <div className="flex justify-between items-center px-1">
        <h3 className="text-sm font-medium text-gray-500">
          <span className="font-bold text-gray-900">{MOCK_DATA.length}</span> sonuç bulundu
        </h3>
      </div>

      <div className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-50 text-gray-500 font-medium text-xs uppercase tracking-wider border-b border-gray-200">
              <tr>
                <th className="px-4 py-4 w-10">FAV</th>
                <th className="px-4 py-4">KURUM & FAKÜLTE</th>
                <th className="px-4 py-4">PROGRAM</th>
                <th className="px-4 py-4">ŞEHİR</th>
                <th className="px-4 py-4">YIL</th>
                <th className="px-4 py-4 text-right">KONTENJAN</th>
                <th className="px-4 py-4 text-right">YERLEŞEN</th>
                <th className="px-4 py-4 text-right">TABAN PUAN</th>
                <th className="px-4 py-4 text-right">TAVAN PUAN</th>
                <th className="px-4 py-4 text-center">İŞLEMLER</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {MOCK_DATA.map((row) => (
                <tr key={row.id} className="hover:bg-blue-50/50 transition-colors group">
                  <td className="px-4 py-4">
                    <button className="text-gray-400 hover:text-red-500 transition-colors">
                      <Heart className="w-5 h-5" />
                    </button>
                  </td>
                  <td className="px-4 py-4">
                    <p className="font-semibold text-gray-900">{row.institution}</p>
                    <p className="text-xs text-gray-500 mt-0.5">{row.ministry}</p>
                  </td>
                  <td className="px-4 py-4">
                    <p className="font-medium text-gray-900">{row.program}</p>
                    <p className="text-xs text-gray-500 mt-0.5">{row.level}</p>
                  </td>
                  <td className="px-4 py-4 text-gray-600">{row.city}</td>
                  <td className="px-4 py-4 text-gray-600 font-medium">{row.period}</td>
                  <td className="px-4 py-4 text-right font-medium text-gray-900">{row.quota}</td>
                  <td className="px-4 py-4 text-right font-medium text-gray-900">{row.placed}</td>
                  <td className="px-4 py-4 text-right font-semibold text-gray-900">{row.minScore.toFixed(2)}</td>
                  <td className="px-4 py-4 text-right text-gray-600">{row.maxScore.toFixed(2)}</td>
                  <td className="px-4 py-4 text-center">
                    <button className="px-3 py-1.5 text-xs font-medium text-blue-700 bg-white border border-blue-200 rounded hover:bg-blue-50 transition-colors">
                      Detay &gt;
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
