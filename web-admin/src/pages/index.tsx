"use client";

import React from "react";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-white text-black p-8">
      <h1 className="text-4xl font-bold mb-4">DjibRide Admin Dashboard</h1>
      <p className="text-lg mb-8">
        Bienvenue sur le tableau de bord administrateur de DjibRide.
      </p>
      <div className="w-full max-w-4xl space-y-6">
        <section className="p-6 border border-gray-300 rounded-lg shadow-sm">
          <h2 className="text-2xl font-semibold mb-2">Statistiques</h2>
          <p>Nombre de chauffeurs actifs, clients, courses, etc.</p>
        </section>
        <section className="p-6 border border-gray-300 rounded-lg shadow-sm">
          <h2 className="text-2xl font-semibold mb-2">Gestion des utilisateurs</h2>
          <p>Clients, chauffeurs, vérification des documents, etc.</p>
        </section>
        <section className="p-6 border border-gray-300 rounded-lg shadow-sm">
          <h2 className="text-2xl font-semibold mb-2">Paiements & Tarifs</h2>
          <p>Gestion des paiements, retraits, tarifs par km et type de service.</p>
        </section>
        <section className="p-6 border border-gray-300 rounded-lg shadow-sm">
          <h2 className="text-2xl font-semibold mb-2">Support client</h2>
          <p>Chat 24/7 intégré pour assistance et signalements.</p>
        </section>
      </div>
    </main>
  );
}
