# 📚 Dokumentasi Lengkap ERD Builder - Logic & Algoritma

## Daftar Isi
1. [Pengantar](#pengantar)
2. [Konsep Dasar Koordinat](#konsep-dasar-koordinat)
3. [Penempatan Entitas](#penempatan-entitas)
4. [Penempatan Atribut](#penempatan-atribut)
5. [Spacing dan Jarak](#spacing-dan-jarak)
6. [Contoh Simulasi Perhitungan](#contoh-simulasi-perhitungan)

---

## Pengantar

File `erd-builder.js` bertanggung jawab untuk:
- **Menghitung posisi entitas** dalam diagram ERD
- **Mendistribusikan atribut** di sekitar entitas
- **Menghindari overlap** antara atribut dan garis relasi
- **Mengatur spacing** antara elemen-elemen diagram

Kode ini menggunakan **Graphviz (layout engine neato)** yang bekerja dengan **sistem koordinat Cartesian 2D**.

---

## Konsep Dasar Koordinat

### Sistem Koordinat Graphviz

```
        Y
        ↑
        |
        |
   (-x,+y) | (+x,+y)
        |
--------+-------→ X
        |
   (-x,-y) | (+x,-y)
        |
```

**Karakteristik:**
- **Titik pusat (0, 0)**: Biasanya entitas pertama/root
- **Sumbu X positif**: Ke kanan
- **Sumbu Y positif**: Ke atas
- **Unit**: Satuan inch (Graphviz default)

### Konversi Sudut ke Radian

Banyak perhitungan menggunakan fungsi trigonometri yang memerlukan radian:

```javascript
angleRad = (angle * Math.PI) / 180
```

**Contoh:**
- 0° → 0 radian → Arah kanan (→)
- 90° → π/2 radian → Arah atas (↑)
- 180° → π radian → Arah kiri (←)
- 270° → 3π/2 radian → Arah bawah (↓)

### Perhitungan Posisi Melingkar

Untuk menempatkan atribut di sekitar entitas dalam pola melingkar:

```javascript
x = centerX + radius * Math.cos(angleRad)
y = centerY + radius * Math.sin(angleRad)
```

**Visualisasi:**
```
          atribut_atas (90°)
               |
               |
   atribut_kiri (180°) --- [ENTITAS] --- atribut_kanan (0°)
               |
               |
         atribut_bawah (270°)
```

---

## Penempatan Entitas

### Fungsi: `calculateEntityPositions()`

Fungsi ini menghitung posisi setiap entitas berdasarkan relasi antar-entitas.

#### 1. Penentuan Spacing

```javascript
let xSpacing, ySpacing;

if (numEntities >= 15) {
    xSpacing = 8;  // Jarak horizontal antar entitas
    ySpacing = 6;  // Jarak vertikal antar entitas
} else if (numEntities >= 4) {
    xSpacing = 6;
    ySpacing = 4;
} else {
    xSpacing = 5;
    ySpacing = 3;
}
```

**Logika:** Semakin banyak entitas, semakin besar spacing untuk menghindari overlap.

#### 2. Membangun Graf Relasi

```javascript
const relGraph = {}; // Adjacency list

relationships.forEach(rel => {
    const e1 = rel.entity1;
    const e2 = rel.entity2;
    const layout = rel.layout; // 'TB', 'LR', 'BT', 'RL'
    
    if (!relGraph[e1]) relGraph[e1] = [];
    if (!relGraph[e2]) relGraph[e2] = [];
    
    relGraph[e1].push({ to: e2, layout: layout });
    
    // Relasi bersifat bidirectional
    const reverseLayout = {
        'LR': 'RL',  // Left-Right → Right-Left
        'RL': 'LR',
        'TB': 'BT',  // Top-Bottom → Bottom-Top
        'BT': 'TB'
    }[layout];
    relGraph[e2].push({ to: e1, layout: reverseLayout });
});
```

**Contoh Graf:**
```
Entitas A ---LR---> Entitas B
Entitas A ---TB---> Entitas C

relGraph = {
    'A': [
        { to: 'B', layout: 'LR' },
        { to: 'C', layout: 'TB' }
    ],
    'B': [
        { to: 'A', layout: 'RL' }
    ],
    'C': [
        { to: 'A', layout: 'BT' }
    ]
}
```

#### 3. Penentuan Root (Entitas Awal)

```javascript
let root = null;

// Prioritas: Entitas dengan relasi vertikal (TB/BT)
for (const rel of relationships) {
    if (['TB', 'BT'].includes(rel.layout)) {
        root = rel.entity1;
        break;
    }
}

// Fallback: Entitas pertama
if (!root && entities.length > 0) {
    root = entities[0].name;
}

// Set posisi root di titik pusat (0, 0)
if (root) {
    positions[root] = { x: 0, y: 0 };
    placed.add(root);
}
```

**Alasan:** Relasi vertikal biasanya adalah hierarki utama (parent-child).

#### 4. Algoritma BFS (Breadth-First Search)

Penempatan entitas menggunakan **BFS** untuk menjelajahi graf relasi:

```javascript
const queue = [root];

while (queue.length > 0) {
    const current = queue.shift();
    const currentPos = positions[current];
    
    relGraph[current].forEach(conn => {
        const target = conn.to;
        const layout = conn.layout;
        
        if (!placed.has(target)) {
            let newPos = { x: 0, y: 0 };
            
            switch (layout) {
                case 'TB': // Top-Bottom: target di bawah current
                    newPos = { 
                        x: currentPos.x, 
                        y: currentPos.y - ySpacing 
                    };
                    break;
                    
                case 'BT': // Bottom-Top: target di atas current
                    newPos = { 
                        x: currentPos.x, 
                        y: currentPos.y + ySpacing 
                    };
                    break;
                    
                case 'LR': // Left-Right: target di kanan current
                    newPos = { 
                        x: currentPos.x + xSpacing, 
                        y: currentPos.y 
                    };
                    break;
                    
                case 'RL': // Right-Left: target di kiri current
                    newPos = { 
                        x: currentPos.x - xSpacing, 
                        y: currentPos.y 
                    };
                    break;
            }
            
            positions[target] = newPos;
            placed.add(target);
            queue.push(target);
        }
    });
}
```

**Visualisasi Proses BFS:**
```
Iterasi 0: Root A di (0, 0)
           [A]
           
Iterasi 1: Process A → tambah B (LR) dan C (TB)
           [A] --→ [B]
            ↓
           [C]
           
Iterasi 2: Process B → tambah D (TB)
           [A] --→ [B]
            ↓       ↓
           [C]     [D]
```

#### 5. Menangani Entitas Tidak Terhubung

```javascript
const unconnected = entities.filter(entity => 
    !placed.has(entity.name)
);

if (unconnected.length > 0 && placed.size > 0) {
    // Cari batas diagram yang sudah ada
    const placedPositions = Array.from(placed).map(name => positions[name]);
    const minX = Math.min(...placedPositions.map(p => p.x));
    const maxX = Math.max(...placedPositions.map(p => p.x));
    const minY = Math.min(...placedPositions.map(p => p.y));
    const maxY = Math.max(...placedPositions.map(p => p.y));
    
    // Tempatkan di bawah diagram utama
    const startX = minX;
    const startY = maxY + ySpacing * 1.5; // Extra spacing
    
    unconnected.forEach((entity, idx) => {
        positions[entity.name] = {
            x: startX + (idx * xSpacing),
            y: startY
        };
    });
}
```

**Visualisasi:**
```
Diagram utama:
    [A] --→ [B]
     ↓       ↓
    [C]     [D]

Entitas unconnected (E, F):
    [A] --→ [B]
     ↓       ↓
    [C]     [D]
    
    (extra spacing)
    
    [E]     [F]
```

---

## Penempatan Atribut

### Fungsi: `distributeAttributes(entityName, entityPos, attrs, positions)`

Fungsi ini adalah **inti** dari penempatan atribut yang kompleks.

### 1. Mendapatkan Arah Relasi

```javascript
function getRelationshipDirections(entityName, positions) {
    const directions = [];
    const entityPos = positions[entityName];
    
    relationships.forEach(rel => {
        let otherEntity = null;
        
        if (rel.entity1 === entityName) {
            otherEntity = rel.entity2;
        } else if (rel.entity2 === entityName) {
            otherEntity = rel.entity1;
        }
        
        if (otherEntity && positions[otherEntity]) {
            const otherPos = positions[otherEntity];
            
            // Hitung vektor dari entityPos ke otherPos
            const dx = otherPos.x - entityPos.x;
            const dy = otherPos.y - entityPos.y;
            
            // Hitung sudut dalam derajat
            const angle = Math.atan2(dy, dx) * (180 / Math.PI);
            
            // Hitung jarak
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            directions.push({ angle, distance, entity: otherEntity });
        }
    });
    
    return directions;
}
```

**Penjelasan Math.atan2:**
- `Math.atan2(dy, dx)` menghitung sudut dari sumbu X positif ke vektor (dx, dy)
- Hasilnya dalam **radian** dari -π hingga π
- Konversi ke **derajat** dengan `* (180 / Math.PI)`

**Contoh:**
```
Entitas A di (0, 0)
Entitas B di (6, 0)  → dx=6, dy=0  → angle = 0°   (kanan)
Entitas C di (0, -4) → dx=0, dy=-4 → angle = -90° (bawah)
Entitas D di (-6, 0) → dx=-6, dy=0 → angle = 180° (kiri)
```

### 2. Deteksi Orientasi Relasi

```javascript
let verticalRelations = 0;
let horizontalRelations = 0;

relDirections.forEach(relDir => {
    const angle = Math.abs(relDir.angle);
    
    // Vertikal: 60-120° atau 240-300°
    if ((angle >= 60 && angle <= 120) || 
        (angle >= 240 && angle <= 300)) {
        verticalRelations++;
    } 
    // Horizontal: 0-30°, 150-210°, atau 330-360°
    else if ((angle <= 30) || 
             (angle >= 150 && angle <= 210) || 
             (angle >= 330)) {
        horizontalRelations++;
    }
});

const isVerticalDominant = verticalRelations > horizontalRelations;
const isMixedOrientation = verticalRelations > 0 && horizontalRelations > 0;
```

**Visualisasi Range Sudut:**
```
        90° (atas)
         |
         | Vertical
    60°  |  120°
        \|/
---------+---------  0°/360° (kanan)
        /|\
   240° | 270° (bawah)
        |
        | Vertical
       300°

Horizontal: 0-30°, 150-210° (kiri), 330-360°
```

### 3. Penentuan Base Radius dan Clearance

```javascript
let baseRadius, clearance;

if (numEntities >= 15) {
    baseRadius = 1.8;  // Jarak dasar atribut dari entitas
    clearance = 40;    // Zona terlarang (derajat)
} else if (numEntities >= 4) {
    baseRadius = 1.3;
    clearance = 35;
} else {
    baseRadius = 1.3;
    clearance = 30;
}
```

**baseRadius**: Jarak dari pusat entitas ke atribut (dalam inch).
**clearance**: Area yang diblock di sekitar garis relasi (dalam derajat).

### 4. Adaptive Radius Multiplier (INTI OPTIMASI)

Ini adalah bagian paling kompleks yang mengatur radius berdasarkan kondisi:

#### Kondisi 1: Super High-Density (4+ relasi, 10+ atribut)

```javascript
if (numRelations >= 4 && numAttrs >= 10) {
    clearance = Math.max(16, clearance * 0.55);
    radiusMultiplier = 0.75;
}
```

**Alasan:**
- **4+ relasi** memblock banyak area (atas, bawah, kiri, kanan)
- **10+ atribut** perlu ruang sangat banyak
- **Radius dikurangi agresif (0.75x)** agar atribut lebih rapat

**Visualisasi:**
```
    rel_atas
        |
 rel_kiri---[ENTITAS]---rel_kanan
        |
    rel_bawah
    
10 atribut harus muat di sela-sela 4 relasi!
```

#### Kondisi 2: High-Density (4+ relasi, 8-9 atribut)

```javascript
else if (numRelations >= 4 && numAttrs > 7) {
    clearance = Math.max(18, clearance * 0.6);
    radiusMultiplier = 0.80;
}
```

**Radius sedikit lebih besar** dari kondisi super padat.

#### Kondisi 3: Mixed Orientation (3+ relasi, 5+ atribut)

```javascript
else if (numRelations >= 3 && numAttrs >= 5) {
    if (isVerticalDominant && isMixedOrientation) {
        // Vertical + Horizontal
        clearance = Math.max(22, clearance * 0.7);
        radiusMultiplier = 0.85;
    } 
    else if (isVerticalDominant) {
        // Pure Vertical
        clearance = Math.max(15, clearance * 0.5);
        radiusMultiplier = 0.75;
    } 
    else {
        // Horizontal Dominant
        clearance = Math.max(20, clearance * 0.65);
        radiusMultiplier = 0.90;
    }
}
```

**Alasan:**
- **Mixed orientation** perlu clearance lebih besar untuk horizontal
- **Pure vertical** bisa lebih rapat karena atribut bisa di kiri/kanan
- **Horizontal dominant** perlu clearance moderat

#### Kondisi 4: 2 Relasi dengan 5+ Atribut

```javascript
else if (numRelations == 2 && numAttrs >= 5) {
    if (isMixedOrientation) {
        if (numAttrs == 6) {
            // Kasus khusus 6 atribut
            clearance = Math.max(25, clearance * 0.75);
            radiusMultiplier = 0.88;
        } else {
            clearance = Math.max(22, clearance * 0.7);
            radiusMultiplier = 0.92;
        }
    } 
    // ... kondisi lainnya
}
```

**6 atribut dapat treatment khusus** karena distribusi genap bermasalah.

#### Kondisi 5: Default

```javascript
else if (numAttrs >= 1) {
    radiusMultiplier = 0.92; // Reduction ringan
}
```

**Semua entitas pasti mendapat reduction** untuk mencegah zoom out.

### 5. Membuat Zona Terlarang (Blocked Ranges)

```javascript
const blockedRanges = [];

relDirections.forEach(relDir => {
    const angle = ((relDir.angle % 360) + 360) % 360; // Normalize 0-360
    
    let effectiveClearance = clearance;
    
    // Extra clearance untuk horizontal pada kondisi tertentu
    if ((isMixedOrientation && numAttrs >= 5) || 
        (numRelations == 1 && numAttrs >= 6)) {
        
        const isHorizontal = (absAngle <= 30) || 
                            (absAngle >= 150 && absAngle <= 210) || 
                            (absAngle >= 330);
        
        if (isHorizontal) {
            const multiplier = /* kondisi */ ? 1.8 : 1.5;
            effectiveClearance = clearance * multiplier;
        }
    }
    
    // Buat range terlarang
    const startBlock = ((angle - effectiveClearance) % 360 + 360) % 360;
    const endBlock = ((angle + effectiveClearance) % 360 + 360) % 360;
    
    blockedRanges.push({ start: startBlock, end: endBlock });
});
```

**Visualisasi Blocked Range:**
```
Relasi ke kanan (0°), clearance = 30°:

      330° --|-- 30°  (zona terlarang)
            /|\
           / | \
          /  |  \
        /   [E]---→ relasi
        
Atribut TIDAK boleh ditempatkan di 330-30°
```

### 6. Mencari Sudut yang Tersedia

```javascript
const candidateAngles = [];

for (let angle = 0; angle < 360; angle += 10) {
    let isBlocked = false;
    
    for (const range of blockedRanges) {
        if (range.start <= range.end) {
            // Normal range: 60-120
            if (angle >= range.start && angle <= range.end) {
                isBlocked = true;
                break;
            }
        } else {
            // Wrap-around range: 330-30 (melewati 0°)
            if (angle >= range.start || angle <= range.end) {
                isBlocked = true;
                break;
            }
        }
    }
    
    if (!isBlocked) {
        candidateAngles.push(angle);
    }
}
```

**Penjelasan Wrap-around:**
```
Range 330-30° melewati 0°:

360° ---|--- 0°
    330 | 30
        |
        
Angle 350° → isBlocked = true (350 >= 330)
Angle 20°  → isBlocked = true (20 <= 30)
Angle 180° → isBlocked = false
```

### 7. Memilih Sudut untuk Atribut

```javascript
const selectedAngles = [];

if (numAttrs <= availableAngles.length) {
    // Distribusi merata
    const step = availableAngles.length / numAttrs;
    
    for (let i = 0; i < numAttrs; i++) {
        selectedAngles.push(
            availableAngles[Math.floor(i * step)]
        );
    }
} else {
    // Terlalu banyak atribut, gunakan semua angle
    selectedAngles.push(...availableAngles);
    
    // Sisanya di sudut default (90°)
    while (selectedAngles.length < numAttrs) {
        selectedAngles.push(90);
    }
}
```

**Contoh Distribusi:**
```
availableAngles = [60, 70, 80, 100, 110, 120, 240, 250, 260, 280, 290, 300]
(12 sudut tersedia)

numAttrs = 4:
step = 12 / 4 = 3
selectedAngles = [60, 100, 240, 280]
(setiap atribut berjarak ~3 slot)

numAttrs = 6:
step = 12 / 6 = 2
selectedAngles = [60, 80, 110, 240, 260, 290]
```

### 8. Menghitung Posisi Final Atribut

```javascript
attrs.forEach((attr, i) => {
    const angle = selectedAngles[i];
    const angleRad = (angle * Math.PI) / 180;
    
    // Variance untuk variasi jarak
    let radiusVariance;
    
    if (numRelations >= 4 && numAttrs >= 10) {
        radiusVariance = (i % 2) * 0.03; // 0, 0.03, 0, 0.03
    } 
    else if (numRelations >= 4 && numAttrs >= 7) {
        radiusVariance = (i % 2) * 0.05;
    } 
    else if ((numRelations == 2 && numAttrs == 6 && isMixedOrientation) || 
             (numRelations == 1 && numAttrs >= 6)) {
        radiusVariance = (i % 2) * 0.08;
    } 
    else if (numAttrs >= 2 && numAttrs <= 4) {
        radiusVariance = (i % 2) * 0.06;
    } 
    else {
        radiusVariance = (i % 3) * 0.10; // 0, 0.10, 0.20
    }
    
    // Hitung radius final
    const radius = baseRadius * radiusMultiplier * (1.0 + radiusVariance);
    
    // Hitung posisi Cartesian
    const attrX = entityPos.x + radius * Math.cos(angleRad);
    const attrY = entityPos.y + radius * Math.sin(angleRad);
    
    attrPositions[attr] = { x: attrX, y: attrY };
});
```

**Penjelasan Radius Variance:**
- Memberikan **variasi kecil** pada jarak atribut
- Pattern `(i % 2)` atau `(i % 3)` membuat **pola alternating**
- Mencegah atribut terlalu sejajar yang terlihat kaku

**Contoh:**
```
baseRadius = 1.3
radiusMultiplier = 0.88
radiusVariance untuk i=0,1,2,3,4,5 dengan pattern (i % 2) * 0.08:
  i=0: variance = 0.00 → radius = 1.3 * 0.88 * 1.00 = 1.144
  i=1: variance = 0.08 → radius = 1.3 * 0.88 * 1.08 = 1.236
  i=2: variance = 0.00 → radius = 1.3 * 0.88 * 1.00 = 1.144
  i=3: variance = 0.08 → radius = 1.3 * 0.88 * 1.08 = 1.236
  i=4: variance = 0.00 → radius = 1.3 * 0.88 * 1.00 = 1.144
  i=5: variance = 0.08 → radius = 1.3 * 0.88 * 1.08 = 1.236
```

---

## Spacing dan Jarak

### Entity Spacing

| Jumlah Entitas | xSpacing | ySpacing | Alasan |
|----------------|----------|----------|--------|
| < 4 | 5 | 3 | Diagram kecil, spacing normal |
| 4-14 | 6 | 4 | Diagram sedang, perlu ruang lebih |
| ≥ 15 | 8 | 6 | Diagram besar, spacing maksimal |

### Attribute Spacing (Base Radius)

| Jumlah Entitas | Base Radius | Alasan |
|----------------|-------------|--------|
| < 4 | 1.3 | Kompak |
| 4-14 | 1.3 | Kompak |
| ≥ 15 | 1.8 | Lebih longgar untuk diagram besar |

### Radius Multiplier Summary

| Kondisi | Multiplier | Variance Max | Contoh |
|---------|------------|--------------|--------|
| 4+ relasi, 10+ atribut | 0.75 | 0.03 | Penduduk (4 relasi, 10 atribut) |
| 4+ relasi, 8-9 atribut | 0.80 | 0.05 | Penduduk (4 relasi, 8 atribut) |
| 3+ relasi, 5+ atribut (mixed) | 0.85 | 0.10 | Produksi (3 relasi mixed, 5 atribut) |
| 2 relasi, 6 atribut (mixed) | 0.88 | 0.08 | Pegawai (2 relasi, 6 atribut) |
| 1 relasi, 5+ atribut | 0.88 | 0.08 | Obat (1 relasi, 6 atribut) |
| 2-4 atribut | 0.90 | 0.06 | Entitas kecil |
| Default (1+ atribut) | 0.92 | 0.10 | Semua lainnya |

---

## Contoh Simulasi Perhitungan

### Skenario: Entitas "Pegawai" dengan 2 Relasi dan 6 Atribut

**Setup:**
- Entitas: Pegawai
- Posisi: (0, 0)
- Relasi: 1 ke kanan (0°), 1 ke bawah (-90°)
- Atribut: ["id", "nama", "alamat", "gaji", "no_telp", "email"]
- Total entitas diagram: 5

#### Langkah 1: Tentukan Base Parameters

```javascript
numEntities = 5
numRelations = 2
numAttrs = 6

// Karena numEntities = 5 (4-14 range):
baseRadius = 1.3
clearance = 35
```

#### Langkah 2: Deteksi Orientasi Relasi

```javascript
relDirections = [
    { angle: 0, distance: 6, entity: "Departemen" },    // Horizontal (kanan)
    { angle: -90, distance: 4, entity: "Proyek" }       // Vertikal (bawah)
]

// Analisis:
// angle = 0° → |0| = 0 → 0 <= 30 → horizontalRelations++
// angle = -90° → |-90| = 90 → 60 <= 90 <= 120 → verticalRelations++

verticalRelations = 1
horizontalRelations = 1
isVerticalDominant = false (1 > 1 = false)
isMixedOrientation = true (1 > 0 && 1 > 0)
```

#### Langkah 3: Tentukan Radius Multiplier

```javascript
// Kondisi: numRelations == 2 && numAttrs >= 5
// Sub-kondisi: isMixedOrientation && numAttrs == 6

clearance = Math.max(25, 35 * 0.75) = Math.max(25, 26.25) = 26.25°
radiusMultiplier = 0.88
```

#### Langkah 4: Buat Blocked Ranges

```javascript
// Relasi 1: angle = 0°
angle = ((0 % 360) + 360) % 360 = 0
absAngle = 0

// Cek horizontal: absAngle = 0 <= 30 → true
// Kondisi extra clearance: isMixedOrientation && numAttrs >= 5 → true
// numRelations == 2 && numAttrs == 6 → true → multiplier = 1.8

effectiveClearance1 = 26.25 * 1.8 = 47.25°

startBlock1 = ((0 - 47.25) % 360 + 360) % 360 = 312.75°
endBlock1 = ((0 + 47.25) % 360 + 360) % 360 = 47.25°

blockedRange1 = { start: 312.75, end: 47.25 } // Wrap-around


// Relasi 2: angle = -90°
angle = ((-90 % 360) + 360) % 360 = 270
absAngle = 90

// Cek horizontal: 90 tidak memenuhi kondisi horizontal
// effectiveClearance2 = 26.25° (default)

startBlock2 = ((270 - 26.25) % 360 + 360) % 360 = 243.75°
endBlock2 = ((270 + 26.25) % 360 + 360) % 360 = 296.25°

blockedRange2 = { start: 243.75, end: 296.25 }
```

**Visualisasi Blocked Zones:**
```
        90°
         |
         |
    120°| 60°
        |
--------+--------- 0° (RELASI 1: BLOCKED 312.75-47.25°)
        |
        |
   240° |270° (RELASI 2: BLOCKED 243.75-296.25°)
        |
       300°

Available zones: 47.25-243.75° (sekitar 196.5° area!)
```

#### Langkah 5: Cari Sudut Tersedia

```javascript
candidateAngles = [];

for (angle = 0; angle < 360; angle += 10) {
    // Cek angle 0: 
    // Range 1 (312.75-47.25): 0 >= 312.75? No. 0 <= 47.25? Yes → BLOCKED
    
    // Cek angle 10:
    // Range 1: 10 <= 47.25? Yes → BLOCKED
    
    // Cek angle 50:
    // Range 1: 50 >= 312.75? No. 50 <= 47.25? No → OK
    // Range 2: 50 >= 243.75 && 50 <= 296.25? No → OK
    // candidateAngles.push(50)
    
    // ... dst
}

candidateAngles = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 
                   160, 170, 180, 190, 200, 210, 220, 230, 240]
// Total: 20 sudut tersedia
```

#### Langkah 6: Pilih Sudut untuk 6 Atribut

```javascript
numAttrs = 6
availableAngles.length = 20

step = 20 / 6 = 3.333

selectedAngles = [
    availableAngles[Math.floor(0 * 3.333)] = availableAngles[0] = 50,
    availableAngles[Math.floor(1 * 3.333)] = availableAngles[3] = 80,
    availableAngles[Math.floor(2 * 3.333)] = availableAngles[6] = 110,
    availableAngles[Math.floor(3 * 3.333)] = availableAngles[10] = 150,
    availableAngles[Math.floor(4 * 3.333)] = availableAngles[13] = 180,
    availableAngles[Math.floor(5 * 3.333)] = availableAngles[16] = 210
]

selectedAngles = [50, 80, 110, 150, 180, 210]
```

#### Langkah 7: Hitung Posisi Final

```javascript
attrs = ["id", "nama", "alamat", "gaji", "no_telp", "email"]

// Kondisi variance: numRelations == 2 && numAttrs == 6 && isMixedOrientation
// radiusVariance = (i % 2) * 0.08

// Atribut 0: "id"
i = 0
angle = 50°
angleRad = 50 * (3.14159 / 180) = 0.8727 radian
radiusVariance = (0 % 2) * 0.08 = 0.00
radius = 1.3 * 0.88 * (1.0 + 0.00) = 1.144

attrX = 0 + 1.144 * cos(0.8727) = 0 + 1.144 * 0.6428 = 0.735
attrY = 0 + 1.144 * sin(0.8727) = 0 + 1.144 * 0.7660 = 0.876

positions["id"] = { x: 0.735, y: 0.876 }


// Atribut 1: "nama"
i = 1
angle = 80°
angleRad = 1.3963 radian
radiusVariance = (1 % 2) * 0.08 = 0.08
radius = 1.3 * 0.88 * (1.0 + 0.08) = 1.236

attrX = 0 + 1.236 * cos(1.3963) = 0 + 1.236 * 0.1736 = 0.215
attrY = 0 + 1.236 * sin(1.3963) = 0 + 1.236 * 0.9848 = 1.218

positions["nama"] = { x: 0.215, y: 1.218 }


// Atribut 2: "alamat"
i = 2
angle = 110°
angleRad = 1.9199 radian
radiusVariance = (2 % 2) * 0.08 = 0.00
radius = 1.144

attrX = 0 + 1.144 * cos(1.9199) = 0 + 1.144 * (-0.3420) = -0.391
attrY = 0 + 1.144 * sin(1.9199) = 0 + 1.144 * 0.9397 = 1.075

positions["alamat"] = { x: -0.391, y: 1.075 }


// Atribut 3: "gaji"
i = 3
angle = 150°
angleRad = 2.6180 radian
radiusVariance = (3 % 2) * 0.08 = 0.08
radius = 1.236

attrX = 0 + 1.236 * cos(2.6180) = 0 + 1.236 * (-0.8660) = -1.070
attrY = 0 + 1.236 * sin(2.6180) = 0 + 1.236 * 0.5000 = 0.618

positions["gaji"] = { x: -1.070, y: 0.618 }


// Atribut 4: "no_telp"
i = 4
angle = 180°
angleRad = 3.1416 radian
radiusVariance = (4 % 2) * 0.08 = 0.00
radius = 1.144

attrX = 0 + 1.144 * cos(3.1416) = 0 + 1.144 * (-1.0) = -1.144
attrY = 0 + 1.144 * sin(3.1416) = 0 + 1.144 * 0.0 = 0.000

positions["no_telp"] = { x: -1.144, y: 0.000 }


// Atribut 5: "email"
i = 5
angle = 210°
angleRad = 3.6652 radian
radiusVariance = (5 % 2) * 0.08 = 0.08
radius = 1.236

attrX = 0 + 1.236 * cos(3.6652) = 0 + 1.236 * (-0.8660) = -1.070
attrY = 0 + 1.236 * sin(3.6652) = 0 + 1.236 * (-0.5000) = -0.618

positions["email"] = { x: -1.070, y: -0.618 }
```

#### Visualisasi Final

```
                nama (80°, 1.218)
                  |
         alamat   |    id
        (110°)    |    (50°)
            \     |     /
             \    |    /
              \   |   /
   gaji -------[PEGAWAI]-------- Departemen (relasi horizontal)
  (150°)        (0,0)
       \         |
        \        |
    no_telp     email      Proyek (relasi vertikal bawah)
     (180°)    (210°)
```

**Perhatikan:**
1. Atribut menghindari arah relasi (0° dan 270°)
2. Distribusi merata di area yang tersedia
3. Variance menciptakan pola alternating (dekat-jauh-dekat-jauh)

---

## Kesimpulan

### Prinsip Utama:

1. **Penempatan Entitas**: BFS berdasarkan graf relasi dengan layout direction (TB, LR, dll)
2. **Penempatan Atribut**: Distribusi melingkar yang menghindari garis relasi
3. **Adaptive Scaling**: Radius dan clearance disesuaikan berdasarkan kompleksitas
4. **Collision Avoidance**: Blocked zones di sekitar relasi
5. **Visual Balance**: Variance untuk variasi jarak yang alami

### Faktor Penentu Layout:

| Faktor | Impact |
|--------|--------|
| Jumlah entitas | Spacing antar entitas |
| Jumlah relasi per entitas | Clearance zone size |
| Jumlah atribut | Radius multiplier |
| Orientasi relasi (V/H/Mixed) | Clearance strategy |
| Density (relasi × atribut) | Aggressive reduction |

### Tips Optimization:

1. **Untuk diagram padat**: Kurangi baseRadius dan radiusMultiplier
2. **Untuk overlap**: Tingkatkan clearance
3. **Untuk zoom out**: Kurangi variance maksimal
4. **Untuk balance**: Sesuaikan spacing berdasarkan numEntities

---

## Referensi

- **Graphviz Documentation**: https://graphviz.org/docs/layouts/neato/
- **Trigonometri**: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math
- **BFS Algorithm**: Algoritma traversal graph untuk penempatan sistematis

---

**Dokumentasi ini dibuat untuk memahami logic kompleks dalam `erd-builder.js`.**
**Untuk pertanyaan lebih lanjut, silakan review kode sumber dengan dokumentasi ini sebagai referensi.**
