# 🗺️ Roadmap Carolina Reminder

## v0.1.0 - MVP (Actual)
✅ Sincronización Google Calendar  
✅ Recordatorios por WhatsApp  
✅ Detección automática de tipos de evento  
✅ Resumen diario  
✅ Notas rápidas  
✅ Marcar eventos completados  
✅ Alertas de plazos críticos  

---

## v0.2.0 - Integración OUCHURUS (Próxima)

**Objetivo:** Integrar OUCHURUS para consultas legales automáticas

- [ ] Agregar endpoint: `POST /api/v1/case/analyze`
  - Envía descripción de caso → OUCHURUS analiza
  - Retorna: jurisprudencia relevante, normativa, plazos
- [ ] Comando WhatsApp: "analizar caso XYZ"
- [ ] Dashboard con casos recientes
- [ ] Integración con SAIJ para jurisprudencia
- [ ] Cálculo automático de plazos procesales

**Ejemplo:**
```
Carolina: "analizar caso García"
Bot: "📑 Caso García (23456/2024)
     ✅ Jurisprudencia relevante: 5 fallos
     ⚖️ Normativa: CC (Art. 402-405 patria potestad)
     ⏰ Próximo vencimiento: 15 días"
```

---

## v0.3.0 - Dashboard Web Completo

- [ ] Panel de login para Carolina
- [ ] Vista calendario interactiva
- [ ] Editar eventos desde web
- [ ] Historial de alertas
- [ ] Estadísticas de casos cerrados
- [ ] Exportar casos en PDF

---

## v0.4.0 - Inteligencia Avanzada

- [ ] IA análisis de descripciones de eventos
- [ ] Recordatorios adaptados si detecta "niebla mental" (pausa entre interacciones)
- [ ] Sugerencias automáticas de documentación
- [ ] Predicción de plazos basada en jurisprudencia

---

## v0.5.0 - Colaboración (Multi-usuario)

**Objetivo:** Agregar abogadas colegas de Carolina

- [ ] Invitar otros usuarios
- [ ] Compartir casos
- [ ] Comentarios en eventos
- [ ] Sistema de permisos
- [ ] Notificaciones de cambios compartidos

---

## v1.0.0 - Producción

- [ ] Documentación completa
- [ ] Tests unitarios
- [ ] Security audit
- [ ] SLA 99.9%
- [ ] Soporte técnico
- [ ] Marketplace de "skills" legales

---

## Features solicitadas recurrentemente

### Por abogadas penalistas (como vos, Adrián)
- [ ] Integración con expedientes judiciales online
- [ ] Alertas de cambio de juzgado/sala
- [ ] Calendario de audiencias automático desde JUBA
- [ ] Cálculo de penas (compatibilidad con OUCHURUS)

### Por abogadas de familia
- [ ] Recordatorios de pagos (pensión alimentaria)
- [ ] Medicinas (custodia, régimen de visitas)
- [ ] Calendario de cumpleaños de menores
- [ ] Seguimiento de mediaciones

### General
- [ ] Integración con WhatsApp Business (números con verificación)
- [ ] Exportar a PDF resumen de casos
- [ ] Análisis de productividad
- [ ] Integración con mail (notificaciones)
- [ ] App mobile nativa (iOS/Android)

---

## Bugs conocidos / Mejoras

- [ ] Parsing de plazos puede mejorar (casos complejos)
- [ ] Zona horaria: hardcodeada a Buenos Aires (hacer configurable)
- [ ] Sincronización puede fallar si token de Google expira
- [ ] WhatsApp sandbox tiene límite de 100 mensajes/día
- [ ] Base de datos sin índices en campos de búsqueda

---

## Métricas a seguir

- % de plazos no olvidados
- Tiempo promedio de respuesta del bot
- Audiencias asistidas / programadas
- Casos cerrados
- Satisfacción de usuario

---

## Colaboradores

Si quieres contribuir:

1. Fork el repo
2. Crea rama: `git checkout -b feature/tu-feature`
3. Commit: `git commit -m "Add: tu feature"`
4. Push: `git push origin feature/tu-feature`
5. Open Pull Request

---

**Last updated:** Junio 2026
