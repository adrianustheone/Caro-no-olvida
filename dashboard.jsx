import React, { useState, useEffect } from 'react';
import { Clock, Calendar, MessageSquare, Settings, Link2, AlertCircle } from 'lucide-react';

export default function CaroNOlvidaDashboard() {
  const [config, setConfig] = useState(null);
  const [events, setEvents] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

  // Fetch data
  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh cada 30s
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [configRes, eventsRes, convRes] = await Promise.all([
        fetch(`${API_BASE}/user/config`),
        fetch(`${API_BASE}/events/upcoming?days=14`),
        fetch(`${API_BASE}/conversations/recent?limit=5`)
      ]);

      if (configRes.ok) setConfig(await configRes.json());
      if (eventsRes.ok) setEvents(await eventsRes.json());
      if (convRes.ok) setConversations(await convRes.json());
      
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const updateReminders = async (hour, nightHour, twoHours) => {
    setSaving(true);
    try {
      const res = await fetch(`${API_BASE}/settings/reminders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          daily_summary_hour: hour,
          reminder_night_before_hour: nightHour,
          reminder_2h_before: twoHours
        })
      });

      if (res.ok) {
        const data = await res.json();
        setConfig(data.settings);
        setTimeout(fetchData, 1000);
      }
    } catch (err) {
      setError(err.message);
    }
    setSaving(false);
  };

  const getEventEmoji = (type) => {
    const emojis = {
      AUDIENCIA: '🏛️',
      PLAZO: '⏰',
      DOCUMENTO: '📋',
      REUNION: '💼',
      OTRO: '📅'
    };
    return emojis[type] || '📅';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando Caro No Olvida...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4 md:p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
                💬 Caro No Olvida
              </h1>
              <p className="text-gray-600 mt-1">Asistente conversacional para Carolina</p>
            </div>
            <div className="flex gap-2 flex-wrap">
              {config?.google_connected ? (
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full flex items-center gap-1 text-sm">
                  <Link2 size={16} /> Google Calendar
                </span>
              ) : (
                <span className="bg-red-100 text-red-800 px-3 py-1 rounded-full flex items-center gap-1 text-sm">
                  <AlertCircle size={16} /> No conectado
                </span>
              )}
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Events & Conversations */}
          <div className="lg:col-span-2 space-y-6">
            {/* Próximos Eventos */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Calendar size={24} /> Próximos Eventos (14 días)
              </h2>
              
              {events.events && events.events.length > 0 ? (
                <div className="space-y-3">
                  {events.events.map((event, idx) => (
                    <div key={idx} className="border-l-4 border-indigo-500 bg-gray-50 p-4 rounded">
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="font-semibold text-gray-800 flex items-center gap-2">
                            {getEventEmoji(event.type)} {event.title}
                          </p>
                          <p className="text-sm text-gray-600 mt-1">
                            📅 {event.date} a las {event.time}
                          </p>
                          {event.juzgado && (
                            <p className="text-sm text-gray-600">🏛️ {event.juzgado}</p>
                          )}
                          {event.case_number && (
                            <p className="text-sm text-gray-600">📑 Caso: {event.case_number}</p>
                          )}
                        </div>
                        <span className="text-xs bg-indigo-100 text-indigo-800 px-2 py-1 rounded">
                          {event.type}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-600 text-center py-8">No hay eventos próximos 🎉</p>
              )}
            </div>

            {/* Conversaciones Recientes */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <MessageSquare size={24} /> Conversaciones Recientes
              </h2>
              
              {conversations.conversations && conversations.conversations.length > 0 ? (
                <div className="space-y-3">
                  {conversations.conversations.map((conv, idx) => (
                    <div key={idx} className="border-l-4 border-blue-400 bg-blue-50 p-4 rounded">
                      <p className="font-semibold text-gray-800">📱 Carolina:</p>
                      <p className="text-gray-700 italic mt-1">"{conv.user_message}"</p>
                      
                      <p className="font-semibold text-gray-800 mt-3">💬 Caro:</p>
                      <p className="text-gray-700 text-sm mt-1">{conv.bot_response?.substring(0, 150)}...</p>
                      
                      <div className="flex justify-between items-center mt-3 text-xs text-gray-500">
                        <span>{new Date(conv.created_at).toLocaleString('es-AR')}</span>
                        <span className={`px-2 py-1 rounded ${
                          conv.status === 'confirmed' ? 'bg-green-100 text-green-800' :
                          conv.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                          'bg-yellow-100 text-yellow-800'
                        }`}>
                          {conv.status}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-600 text-center py-8">Sin conversaciones aún</p>
              )}
            </div>
          </div>

          {/* Right Column - Settings */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
              <Settings size={24} /> Recordatorios
            </h2>

            {config && (
              <div className="space-y-6">
                {/* Resumen Diario */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ⏰ Resumen Diario
                  </label>
                  <div className="flex items-center gap-4">
                    <input
                      type="range"
                      min="0"
                      max="23"
                      value={config.daily_summary_hour}
                      onChange={(e) => {
                        const hour = parseInt(e.target.value);
                        setConfig({ ...config, daily_summary_hour: hour });
                        updateReminders(hour, config.reminder_night_before_hour, config.reminder_2h_before);
                      }}
                      className="w-full"
                    />
                    <span className="text-xl font-bold text-indigo-600 min-w-fit">
                      {config.daily_summary_hour}:00
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-2">
                    Recibirás resumen diario a esta hora
                  </p>
                </div>

                {/* Recordatorio Noche Anterior */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    🌙 Noche Anterior
                  </label>
                  <div className="flex items-center gap-4">
                    <input
                      type="range"
                      min="0"
                      max="23"
                      value={config.reminder_night_before_hour}
                      onChange={(e) => {
                        const hour = parseInt(e.target.value);
                        setConfig({ ...config, reminder_night_before_hour: hour });
                        updateReminders(config.daily_summary_hour, hour, config.reminder_2h_before);
                      }}
                      className="w-full"
                    />
                    <span className="text-xl font-bold text-indigo-600 min-w-fit">
                      {config.reminder_night_before_hour}:00
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 mt-2">
                    Recordatorio la noche anterior a esta hora
                  </p>
                </div>

                {/* Recordatorio 2h Antes */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    ⏱️ Dos Horas Antes
                  </label>
                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => {
                        const newVal = !config.reminder_2h_before;
                        setConfig({ ...config, reminder_2h_before: newVal });
                        updateReminders(config.daily_summary_hour, config.reminder_night_before_hour, newVal);
                      }}
                      className={`px-4 py-2 rounded font-semibold transition-colors ${
                        config.reminder_2h_before
                          ? 'bg-green-500 text-white'
                          : 'bg-gray-300 text-gray-700'
                      }`}
                    >
                      {config.reminder_2h_before ? '✅ Sí' : '❌ No'}
                    </button>
                  </div>
                  <p className="text-xs text-gray-500 mt-2">
                    Recordatorio 2 horas antes de cada evento
                  </p>
                </div>

                {saving && (
                  <p className="text-sm text-blue-600 animate-pulse">💾 Guardando...</p>
                )}

                {/* Info de usuario */}
                <div className="border-t pt-6 mt-6">
                  <p className="text-sm font-semibold text-gray-700">👤 {config.name}</p>
                  <p className="text-xs text-gray-500">📱 {config.whatsapp}</p>
                  <p className="text-xs text-gray-500">🌍 {config.timezone}</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-600 text-sm">
          <p>💪 Caro No Olvida - Para que la fibromialgia no te gane</p>
          <p className="mt-1">Hecho con ❤️ por Adrián</p>
        </div>
      </div>
    </div>
  );
}
