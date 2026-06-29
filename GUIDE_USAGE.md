# 💬 Caro No Olvida - Guía de uso del chat

Bienvenida Carolina! Soy Caro, tu asistente que entiende lenguaje natural por WhatsApp.

---

## 🎯 ¿Cómo funciona?

### 1. **Carolina habla por WhatsApp**
```
Carolina: "Agendar audiencia García mañana 10:00"
```

### 2. **Claude entiende el mensaje**
- Detecta que es un evento
- Extrae: título, fecha, hora
- Identifica: tipo (AUDIENCIA, PLAZO, etc)

### 3. **Se crea en Google Calendar**
- Automáticamente aparece en tu Google Calendar
- Puede verlo visualmente en la app de Google

### 4. **Carolina recibe confirmación por WhatsApp**
```
✅ Evento agendado!

🏛️ Audiencia García
📅 2026-06-28 a las 10:00
📱 También aparece en Google Calendar

💬 Respondé 'confirmar' si está bien o 'cancelar' si cambiaste de idea
```

### 5. **Recordatorios automáticos**
```
Noche anterior (20:00):
🌙 RECORDATORIO NOCHE ANTERIOR
   MAÑANA 10:00 - Audiencia García
   Juzgado: San Martín

Día del evento (2h antes):
⏰ EN 2 HORAS
   Audiencia García 14:00
   ¡MOVE!
```

---

## 💬 Ejemplos de lo que podés decirme

### **Agendar Audiencia**
```
"Audiencia mediación García mañana 10:00"
"Reunión juzgado familia nº3 30 de julio 3pm"
"Audiencia TOC Federal San Martín viernes próximo 14:00"
```

### **Agendar Plazo (Vencimiento)**
```
"Plazo vencimiento recurso apelación 15 de agosto"
"Vencimiento pensión alimentaria 30/7"
"Recurso de casación vence mañana"
```

### **Documentación a presentar**
```
"Presentar escrito demanda viernes próximo"
"Traer sentencia anterior para audiencia García"
"Documento a enviar juzgado 30 de junio"
```

### **Reunión con cliente**
```
"Reunión López martes 3pm"
"Consulta con García jueves 14:00 en mi oficina"
"Meet con cliente penal viernes 16:00"
```

### **Plazos y recordatorios rápidos**
```
"Recordarme traer DNI para audiencia"
"Nota: cliente dijo que se muda 30/7"
"Recordar enviar escritos a tribunal"
```

---

## 🔄 Flujo conversacional

### **Escenario 1: Agendar con información completa**
```
Carolina: "Audiencia García mañana 10:00 juzgado familia San Isidro"

Caro: "✅ Evento agendado!
🏛️ Audiencia García
📅 2026-06-28 a las 10:00
🏛️ Juzgado: Familia San Isidro
📍 San Isidro
📱 También aparece en Google Calendar

💬 Respondé 'confirmar' si está bien o 'cancelar'"

Carolina: "Perfecto"

Caro: "✨ Listo! Recordatorio noche anterior a las 20:00 y 2h antes"
```

### **Escenario 2: Falta información**
```
Carolina: "Agendar audiencia García"

Caro: "🤔 Me falta información.
¿A qué hora es? (ej: 10:00)
¿Qué día? (ej: mañana, jueves, 30 de julio)"

Carolina: "Mañana 10:00"

Caro: "✅ Evento agendado!
🏛️ Audiencia García
📅 2026-06-28 a las 10:00
..."
```

### **Escenario 3: Cambiar de idea**
```
Carolina: "Cancelar"

Caro: "❌ Evento cancelado"
```

---

## 🎯 Comandos especiales

| Comando | Qué hace |
|---------|----------|
| `confirmar` / `ok` / `dale` | Confirma el evento |
| `cancelar` | Cancela el evento |
| `hoy` | Te muestra eventos de hoy |
| `próximos 7 días` | Te muestra próxima semana |
| `nota: ...` | Crea una nota rápida |
| `recordarme ...` | Crea un recordatorio |

---

## 🏛️ Ejemplos del mundo real

### **Caso: Mediación familiar**
```
Carolina: "Agendar mediación caso García martes 10am juzgado familia 3 San Isidro caso 12345/2024"

Caro: "✅ Evento agendado!
🏛️ Mediación García
📅 2026-07-01 a las 10:00
🏛️ Juzgado Familia Nº3
📍 San Isidro
📑 Caso: 12345/2024
ℹ️ Cliente: García

Respondé 'confirmar' para finalizar"

Carolina: "Confirmar"

Caro: "✨ Perfecto! 
Recordatorio: mañana 20:00 y 2h antes"
```

### **Caso: Plazo vencimiento**
```
Carolina: "Plazo vencimiento recurso apelación López caso 54321/2024 15 agosto"

Caro: "✅ Evento agendado!
⏰ PLAZO - Recurso apelación López
📅 2026-08-15
📑 Caso: 54321/2024

Respondé 'confirmar'"

Carolina: "Dale"

Caro: "✨ Listo!
⚠️ Te alertaré: 7 días antes, 3 días antes, 1 día antes, y hoy"
```

---

## 🧠 Cómo entiende Caro

Caro usa **Claude AI** (la misma IA que te ayuda) para entender:

✅ **Lenguaje natural**: "mañana", "próximo jueves", "30 de julio"  
✅ **Variantes**: "10:00", "10am", "10h", las entiende todas  
✅ **Contexto**: "García" → detecta cliente automáticamente  
✅ **Tipos**: "audiencia" → detecta tipo automático  
✅ **Flexibilidad**: Puede rellenar información faltante  

---

## 📱 En tu Google Calendar

Una vez que Caro crea el evento en Google Calendar:

1. **Aparece visual** en tu Google Calendar app
2. **Puedes editarlo** directamente (cambiar hora, agregar nota)
3. **Se sincroniza** automáticamente con Caro
4. **Ves recordatorios** en Google también (además de WhatsApp)

---

## ⚙️ Configuración de recordatorios

**Por defecto:**
- 🌙 Noche anterior: 20:00 (8pm)
- ⏰ 2 horas antes: Sí
- 📋 Resumen diario: 8:00 AM

**Para cambiar:**
Decime por WhatsApp:
```
"Cambiar resumen a las 7am"
"Recordatorio noche anterior a las 19:00"
"Sin recordatorio 2 horas antes"
```

---

## 🔐 Privacidad

- Los datos están en tu servidor (Railway/local)
- Claude procesa el mensaje pero NO lo guarda
- Google Calendar es tuyo (solo vé lo que autorizas)
- Twilio solo envía/recibe WhatsApp
- Nadie más puede ver tu información

---

## 💡 Tips

1. **Sé específica**: Mejor "Audiencia mediación García juzgado 3" que "Audiencia"
2. **Incluye cliente**: Ayuda a identificar el caso
3. **Incluye caso**: "12345/2024" → mejor organización
4. **Confirma**: Siempre confirmá antes de finalizar
5. **Verifica Google Calendar**: Asegurate que aparezca bien visualmente

---

## ❓ Preguntas frecuentes

**P: ¿Caro borra información de Google Calendar?**  
R: No, solo crea eventos. Todo está en Google.

**P: ¿Funciona sin conectar Google Calendar?**  
R: No, necesitás conexión para que Caro cree eventos.

**P: ¿Qué pasa si digo algo raro?**  
R: Caro pregunta para aclarar: "¿A qué hora?"

**P: ¿Puedo editar eventos después?**  
R: Sí, en Google Calendar app, y Caro lo sincroniza.

**P: ¿Funciona sin niebla mental?**  
R: Sí! Caro es útil para cualquiera que hable lenguaje natural.

---

## 🚀 Ya empezaste!

Probá ahora:
```
"Agendar reunión López mañana 3pm"
```

¡Caro entiende! 💪

---

*Caro No Olvida - Tu asistente que escucha*  
*Junio 2026*
