# Arquitectura de Agentes Tuki (Multi-Destino)

## 🏗️ Arquitectura Recomendada: "Granjas por Destino"

### Opción A: Multi-Agente (Recomendada)
Cada destino tiene su "granja":
- `LeadScout-SCL` (Santiago)
- `LeadScout-VLP` (Valparaíso)
- `LeadScout-PUC` (Pucón)
- ... etc

**Ventajas:**
- Especialización por mercado (idioma, cultura, normativas)
- Paralelización: puedo activar 5 destinos al mismo tiempo
- Si uno falla, los otros siguen

### Opción B: Single Agent Multi-Destino
Un LeadScout que rota destinos según backlog.

---

## 📋 Agentes a Crear (Prioridad)

### ✅ Ya existen:
1. **LeadScout** → Encuentra leads
2. **CRMKeeper** → Limpia datos
3. **SalesCloser** → Primer contacto WhatsApp

### 🆕 Nuevos (para empezar PILOTO AUTOMÁTICO):

#### 4. OnboardingAgent 🎯 PRIORIDAD ALTA
**Función**: Llevar relación desde "interesado" hasta "sube info"
**Tareas**:
- Seguimiento post-primer-contacto (SalesCloser pasa el testigo)
- Explicar cómo subir info (por ahora: recolectar por WhatsApp/email)
- Crear JSON intermedio con datos del operador
- Escalar a Tatan cuando operador quiera subir cosas
- Mantener notas de conversación en Notion

#### 5. ContentUploader 🎯 PRIORIDAD ALTA
**Función**: Procesar contenido que operadores envían
**Tareas**:
- Recibir ZIPs de fotos
- Organizar carpetas (alojamiento_X/fotos/, experiencia_Y/fotos/)
- Generar URLs listas para backend
- Asociar fotos a items en Notion

#### 6. DataModeler 🎯 PRIORIDAD MEDIA
**Función**: Conectar con backend Tuki
**Tareas**:
- Recibir datos de OnboardingAgent
- Generar JSON válido según schemas Tuki
- POST a API de Tuki
- Generar preview de cómo se vería en plataforma

---

## 🎯 Objetivo: 1000 items/país

### Metas sugeridas:
| País | Experiencias | Alojamientos | Traslados | Total |
|------|--------------|--------------|-----------|-------|
| Chile | 300 | 500 | 200 | 1000 |
| Argentina | 300 | 500 | 200 | 1000 |
| Perú | 300 | 400 | 300 | 1000 |
| Brasil | 200 | 600 | 200 | 1000 |
| Bolivia | 200 | 400 | 400 | 1000 |

### Destinos prioritarios (20):
Chile: Santiago, Valparaíso, Pucón, San Pedro, Puerto Natales
Argentina: Buenos Aires, Bariloche, Mendoza, Salta, Ushuaia
Perú: Lima, Cusco, Arequipa
Brasil: Río, SP, Florianópolis, Paraty
Bolivia: La Paz, Uyuni

---

## 🔄 Flujo Completo

```
[LeadScout-SCL] → encuentra Hotel X en Santiago
         ↓
[CRMKeeper] → normaliza datos, busca email/tel
         ↓
[SalesCloser] → primer contacto WhatsApp
         ↓
[OnboardingAgent] → "Interesado" → "Comparte info"
         ↓
[ContentUploader] → recibe fotos + datos básicos
         ↓
[DataModeler] → genera JSON → POST a backend Tuki
         ↓
[Tatan] → revisión humana → APROBADO
         ↓
[Tuki Backend] → item publicado
```

---

## 📊 Notion: Estructura de Trabajo

### Base "Leads de captación" (existe):
- Agregar campo: `Destino` (SCL, VLP, etc.)
- Agregar campo: `Agente asignado` (LeadScout-SCL, etc.)
- Agregar campo: `Etapa onboarding` (contactado → interesado → compartiendo_info → listo_para_subir)

### Nueva base: "Piloto Automático" (opcional):
- Items en proceso de carga
- Fotos recibidas pendientes de procesar
- JSONs generados pendientes de aprobación
