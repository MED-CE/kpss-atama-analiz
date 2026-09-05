"use client"

import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';

type YearlyAnalytics = {
  year: number;
  total_quota: number;
  total_placed: number;
  min_score_overall: number | null;
  max_score_overall: number | null;
  cities_count: number;
  institutions_count: number;
};

export default function Dashboard() {
  const [data, setData] = useState<YearlyAnalytics[]>([]);

  useEffect(() => {
    // In a real app, this fetches from NEXT_PUBLIC_API_URL/api/v1/analytics/yearly
    // For now we mock it to show the UI since DB is empty
    setData([
      { year: 2024, total_quota: 5000, total_placed: 4800, min_score_overall: 70.5, max_score_overall: 99.1, cities_count: 81, institutions_count: 150 },
      { year: 2023, total_quota: 12000, total_placed: 11500, min_score_overall: 65.2, max_score_overall: 100.0, cities_count: 81, institutions_count: 210 },
      { year: 2022, total_quota: 8500, total_placed: 8100, min_score_overall: 68.9, max_score_overall: 98.5, cities_count: 81, institutions_count: 180 },
      { year: 2021, total_quota: 6500, total_placed: 6400, min_score_overall: 69.1, max_score_overall: 99.5, cities_count: 81, institutions_count: 165 },
    ].sort((a, b) => a.year - b.year));
  }, []);

  return (
    <div className="space-y-8 w-full">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader><CardTitle>Toplam Kontenjan</CardTitle></CardHeader>
          <CardContent><p className="text-3xl font-bold text-blue-600">{data.reduce((acc, curr) => acc + curr.total_quota, 0).toLocaleString()}</p></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Yerleşen Aday</CardTitle></CardHeader>
          <CardContent><p className="text-3xl font-bold text-green-600">{data.reduce((acc, curr) => acc + curr.total_placed, 0).toLocaleString()}</p></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Kurum Sayısı</CardTitle></CardHeader>
          <CardContent><p className="text-3xl font-bold text-purple-600">210+</p></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>Kapsanan Yıl</CardTitle></CardHeader>
          <CardContent><p className="text-3xl font-bold text-gray-700">2010 - 2024</p></CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <CardHeader><CardTitle>Yıllara Göre Kontenjan ve Yerleşme</CardTitle></CardHeader>
          <CardContent className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data}>
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="total_quota" name="Kontenjan" fill="#3b82f6" />
                <Bar dataKey="total_placed" name="Yerleşen" fill="#10b981" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader><CardTitle>Minimum ve Maksimum Puan Trendi</CardTitle></CardHeader>
          <CardContent className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data}>
                <XAxis dataKey="year" />
                <YAxis domain={['dataMin - 5', 'dataMax + 5']} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="min_score_overall" name="Min Puan" stroke="#f59e0b" strokeWidth={2} />
                <Line type="monotone" dataKey="max_score_overall" name="Max Puan" stroke="#ef4444" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
