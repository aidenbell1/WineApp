import Link from 'next/link';
import { Wine, BarChart3, TrendingUp, Package } from 'lucide-react';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Wine className="h-8 w-8 text-blue-600" />
            <span className="text-2xl font-bold">Sommelier Analytics</span>
          </div>
          <Link
            href="/dashboard"
            className="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700 transition"
          >
            View Dashboard
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-20">
        <div className="text-center max-w-3xl mx-auto">
          <h1 className="text-5xl font-bold mb-6">
            Wine Sales Analytics for Restaurants
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Make data-driven decisions about your wine program without hiring a sommelier.
            Track sales, optimize pricing, and maximize profits.
          </p>
          <Link
            href="/dashboard"
            className="inline-block rounded-lg bg-blue-600 px-8 py-4 text-lg text-white hover:bg-blue-700 transition"
          >
            Get Started
          </Link>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-8 mt-20">
          <div className="p-6 bg-white rounded-lg shadow-sm">
            <BarChart3 className="h-12 w-12 text-blue-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Sales Analytics</h3>
            <p className="text-gray-600">
              Track which wines are selling and identify slow movers instantly.
            </p>
          </div>

          <div className="p-6 bg-white rounded-lg shadow-sm">
            <TrendingUp className="h-12 w-12 text-blue-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Profit Optimization</h3>
            <p className="text-gray-600">
              Analyze margins and get pricing recommendations to maximize profit.
            </p>
          </div>

          <div className="p-6 bg-white rounded-lg shadow-sm">
            <Package className="h-12 w-12 text-blue-600 mb-4" />
            <h3 className="text-xl font-semibold mb-2">Inventory Management</h3>
            <p className="text-gray-600">
              Monitor stock levels and get alerts when it's time to reorder.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
