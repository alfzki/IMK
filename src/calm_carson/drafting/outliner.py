"""Outliner module that formulates structured chapter and subsection hierarchies for STIS thesis proposals and reports."""

from __future__ import annotations

from typing import Dict, List, Optional

from calm_carson.drafting.models import ChapterOutline, SubSectionOutline


class ThesisOutliner:
    """Generates standardized academic chapter outlines aligned with STIS D-IV SIS and IEEE standards."""

    PRESET_TOPICS = {
        "1": {
            "id": "topik_1_survey_fraud",
            "title": "Rancang Bangun Sistem Backend Deteksi Anomali dan Integritas Data Entri Survei Lapangan untuk Mitigasi Falsifikasi Pencacahan BPS",
            "cluster": "data_collection",
            "keywords": ["CAPI", "curbstoning", "dwell time", "Isolation Forest", "HMAC", "BPS", "mitra"],
        },
        "2": {
            "id": "topik_2_sdi_gateway",
            "title": "Rancang Bangun Secure Data Sharing Gateway dan Automasi Validasi Metadata Terdistribusi Berbasis Arsitektur Satu Data Indonesia",
            "cluster": "interoperability_sdi",
            "keywords": ["Satu Data Indonesia", "SDI", "metadata", "EPSS", "IPS", "gateway", "interoperabilitas"],
        },
        "3": {
            "id": "topik_3_differential_privacy",
            "title": "Rancang Bangun Secure On-Demand Microdata Query Engine dengan Penerapan Differential Privacy dan Cryptographic Audit Trail Berbasis API",
            "cluster": "security_privacy",
            "keywords": ["differential privacy", "microdata", "Laplace mechanism", "audit trail", "UU PDP", "BPS"],
        },
    }

    @classmethod
    def get_preset_topics(cls) -> Dict[str, Dict[str, Any]]:
        return cls.PRESET_TOPICS

    def generate_outline(
        self,
        topic_key_or_title: str,
        scope: str = "proposal",
    ) -> List[ChapterOutline]:
        """Generates comprehensive chapter outlines for either a proposal (Bab 1-3) or full thesis (Bab 1-5)."""
        topic_info = self._resolve_topic(topic_key_or_title)
        topic_id = topic_info["id"]

        chapters: List[ChapterOutline] = []

        # Bab I: Pendahuluan
        chapters.append(self._build_chapter_1(topic_info))

        # Bab II: Tinjauan Pustaka
        chapters.append(self._build_chapter_2(topic_info))

        # Bab III: Metodologi Penelitian
        chapters.append(self._build_chapter_3(topic_info))

        if scope.lower() == "thesis":
            # Bab IV: Analisis, Perancangan, dan Evaluasi Sistem
            chapters.append(self._build_chapter_4(topic_info))
            # Bab V: Penutup
            chapters.append(self._build_chapter_5(topic_info))

        return chapters

    def _resolve_topic(self, query: str) -> Dict[str, Any]:
        """Resolves preset key ('1', '2', '3') or custom title into topic metadata."""
        clean_q = str(query).strip()
        if clean_q in self.PRESET_TOPICS:
            return self.PRESET_TOPICS[clean_q]

        for k, v in self.PRESET_TOPICS.items():
            if k == clean_q or v["id"] == clean_q or v["title"].lower() in clean_q.lower():
                return v

        # Custom user topic fallback
        return {
            "id": "custom_thesis_topic",
            "title": query,
            "cluster": "custom",
            "keywords": [w for w in query.split() if len(w) > 3][:6],
        }

    def _build_chapter_1(self, topic: Dict[str, Any]) -> ChapterOutline:
        """Constructs Chapter 1 (Pendahuluan) outline with required 3 empirical problems."""
        t_id = topic.get("id", "")
        if "topik_1" in t_id:
            bg_targets = ["190.000", "3% hingga 15%", "5% hingga 10%", "60%", "45 hingga 75 menit"]
            bg_queries = ["Sensus Pertanian 2023 mitra petugas 190.000", "curbstoning pemalsuan kuesioner", "verifikasi manual PML 5%"]
        elif "topik_2" in t_id:
            bg_targets = ["1,48", "85%", "65%", "400.000"]
            bg_queries = ["Indeks Pembangunan Statistik EPSS 1,48", "metadata Satu Data Indonesia portal", "interoperabilitas OPD BPS"]
        elif "topik_3" in t_id:
            bg_targets = ["2022", "99,98%", "80%", "0,1"]
            bg_queries = ["Undang-Undang PDP No. 27 Tahun 2022", "re-identifikasi data mikro", "differential privacy Laplace BPS"]
        else:
            bg_targets = ["data BPS", "evaluasi empiris", "statistik resmi"]
            bg_queries = topic.get("keywords", [])

        subsections = [
            SubSectionOutline(
                id="1.1",
                title="Latar Belakang Masalah",
                focus_points=[
                    "Urgensi statistik resmi dan proses bisnis GSBPM di Badan Pusat Statistik (BPS)",
                    "Uraian 3 permasalahan konkret pada objek penelitian dengan angka kuantitatif riil dan sitasi resmi",
                    "Rancangan solusi terpadu spesifik untuk mengatasi masing-masing dari ketiga permasalahan",
                ],
                target_quantities=bg_targets,
                search_queries=bg_queries,
                estimated_paragraphs=4,
            ),
            SubSectionOutline(
                id="1.2",
                title="Rumusan Masalah",
                focus_points=[
                    "Identifikasi pertanyaan penelitian perancangan arsitektur sistem berbasis DSRM",
                    "Pertanyaan perancangan modul/algoritma inti",
                    "Pertanyaan evaluasi kualitas perangkat lunak ISO/IEC 25010 dan performa komputasi",
                ],
                search_queries=["rumusan masalah DSRM ISO 25010"],
                estimated_paragraphs=1,
            ),
            SubSectionOutline(
                id="1.3",
                title="Tujuan Penelitian",
                focus_points=[
                    "Tujuan umum dan khusus yang menjawab secara tegas seluruh rumusan masalah",
                    "Target artefak perangkat lunak yang dibangun",
                    "Target metrik evaluasi yang terukur secara kuantitatif",
                ],
                search_queries=["tujuan penelitian artefak sistem"],
                estimated_paragraphs=1,
            ),
            SubSectionOutline(
                id="1.4",
                title="Batasan Masalah",
                focus_points=[
                    "Lingkup data dan objek penelitian (data sensus/survei BPS yang diuji)",
                    "Batasan fungsionalitas sistem (arsitektur backend/gateway/engine)",
                    "Batasan lingkungan pengujian (lingkungan uji non-produksi / data simulasi)",
                ],
                search_queries=["batasan masalah sistem BPS"],
                estimated_paragraphs=1,
            ),
            SubSectionOutline(
                id="1.5",
                title="Manfaat Penelitian",
                focus_points=[
                    "Manfaat teoritis bagi pengembangan keilmuan Komputasi Statistik dan Sistem Informasi Statistik",
                    "Manfaat praktis bagi BPS (Pembina Data) dan Kementerian/Lembaga/Pemerintah Daerah",
                ],
                search_queries=["manfaat penelitian BPS komputasi statistik"],
                estimated_paragraphs=1,
            ),
        ]

        return ChapterOutline(
            id="bab_1",
            number=1,
            title="Pendahuluan",
            academic_goal="Menetapkan landasan masalah nyata berangka empiris, pertanyaan penelitian, dan rancangan solusi artefak sistem.",
            subsections=subsections,
            estimated_words=1600,
        )

    def _build_chapter_2(self, topic: Dict[str, Any]) -> ChapterOutline:
        """Constructs Chapter 2 (Tinjauan Pustaka) outline with required Benchmark Table & Research Gap."""
        subsections = [
            SubSectionOutline(
                id="2.1",
                title="Landasan Teori & Konsep Dasar",
                focus_points=[
                    "Konsep fundamental domain topik (GSBPM, arsitektur sistem, kriptografi/keamanan, statistik resmi)",
                    "Prinsip operasional algoritma dan teknologi perangkat lunak yang diimplementasikan",
                ],
                search_queries=topic.get("keywords", [])[:4],
                estimated_paragraphs=3,
            ),
            SubSectionOutline(
                id="2.2",
                title="Kajian Penelitian Terdahulu (State-of-the-Art)",
                focus_points=[
                    "Telaah publikasi internasional bereputasi (Scopus/IEEE/ACM >= 2021)",
                    "Benchmarking terhadap skripsi alumni D-IV Komputasi Statistik STIS terdahulu",
                ],
                search_queries=[f"skripsi alumni STIS {topic.get('cluster', '')}", "state of the art IEEE"],
                estimated_paragraphs=3,
            ),
            SubSectionOutline(
                id="2.3",
                title="Tabel Kontribusi Penelitian & Benchmarking",
                focus_points=[
                    "Tabel komparasi matriks kontribusi penelitian (Penulis, Tahun, Metode, Kelebihan, Limitasi, Posisi Penelitian Ini)",
                    "Penegasan pembeda teknis (*novelty*) dari penelitian-penelitian sebelumnya",
                ],
                search_queries=["tabel kontribusi penelitian novelty benchmark"],
                estimated_paragraphs=2,
            ),
            SubSectionOutline(
                id="2.4",
                title="Kesenjangan Penelitian (Research Gap), Dampak, & Urgensi",
                focus_points=[
                    "Identifikasi celah teoritis dan batasan praktis yang belum terselesaikan pada penelitian terdahulu",
                    "Dampak konkret bagi akurasi data nasional jika masalah tidak diselesaikan",
                    "Urgensi penyelesaian melalui rekayasa sistem yang diusulkan",
                ],
                search_queries=["kesenjangan penelitian research gap urgensi"],
                estimated_paragraphs=2,
            ),
        ]

        return ChapterOutline(
            id="bab_2",
            number=2,
            title="Tinjauan Pustaka",
            academic_goal="Menyajikan landasan ilmiah, benchmarking karya alumni STIS dan paper internasional, serta menegaskan kesenjangan riset.",
            subsections=subsections,
            estimated_words=2200,
        )

    def _build_chapter_3(self, topic: Dict[str, Any]) -> ChapterOutline:
        """Constructs Chapter 3 (Metodologi Penelitian) outline with DSRM Peffers and ISO 25010."""
        subsections = [
            SubSectionOutline(
                id="3.1",
                title="Desain Penelitian (Design Science Research Methodology / DSRM)",
                focus_points=[
                    "Penerapan 6 tahapan DSRM Peffers et al.: Problem Identification, Objectives, Design & Development, Demonstration, Evaluation, Communication",
                    "Penyelarasan setiap tahapan DSRM dengan fase GSBPM BPS",
                ],
                search_queries=["DSRM Peffers tahapan design science"],
                estimated_paragraphs=2,
            ),
            SubSectionOutline(
                id="3.2",
                title="Sumber Data & Objek Penelitian",
                focus_points=[
                    "Karakteristik data yang digunakan (data sintetis, data sekunder, atau data mikro bertopeng BPS)",
                    "Variabel dan parameter pengujian yang diekstraksi",
                ],
                search_queries=["data mikro survei BPS karakteristik"],
                estimated_paragraphs=2,
            ),
            SubSectionOutline(
                id="3.3",
                title="Perancangan Arsitektur Sistem & Spesifikasi Artefak",
                focus_points=[
                    "Diagram arsitektur sistem tingkat tinggi (Clean Architecture, Microservices, API Gateway)",
                    "Aliran data antar-komponen dari klien hingga repositori basis data",
                ],
                search_queries=["arsitektur sistem perangkat lunak microservices API"],
                estimated_paragraphs=3,
            ),
            SubSectionOutline(
                id="3.4",
                title="Lingkungan Komputasi & Perkakas Pengembangan",
                focus_points=[
                    "Spesifikasi perangkat keras dan sistem operasi pengujian (GPU acceleration, kontainerisasi)",
                    "Tech stack perangkat lunak (Python, FastAPI, SQLite/PostgreSQL, Vue/React)",
                ],
                search_queries=["lingkungan komputasi docker GPU python"],
                estimated_paragraphs=1,
            ),
            SubSectionOutline(
                id="3.5",
                title="Metrik Pengujian & Evaluasi Kualitas Perangkat Lunak",
                focus_points=[
                    "Karakteristik ISO/IEC 25010: Functional Suitability, Performance Efficiency (latensi ms, throughput), Security (OWASP)",
                    "Metrik efektivitas model/algoritma (Precision, Recall, F1-Score, Error Rate)",
                ],
                search_queries=["ISO IEC 25010 pengujian software latensi throughput"],
                estimated_paragraphs=2,
            ),
            SubSectionOutline(
                id="3.6",
                title="Kerangka Pikir Penelitian & Rancangan Jadwal",
                focus_points=[
                    "Bagan alir kerangka pikir penelitian terpadu dari masalah hingga evaluasi",
                    "Rancangan jadwal pelaksanaan penelitian selama 10 bulan (Tabel II)",
                ],
                search_queries=["kerangka pikir jadwal penelitian 10 bulan"],
                estimated_paragraphs=2,
            ),
        ]

        return ChapterOutline(
            id="bab_3",
            number=3,
            title="Metodologi Penelitian",
            academic_goal="Menjabarkan kerangka metodologis DSRM, arsitektur artefak, dan metode evaluasi terukur berstandar ISO/IEC 25010.",
            subsections=subsections,
            estimated_words=2000,
        )

    def _build_chapter_4(self, topic: Dict[str, Any]) -> ChapterOutline:
        """Constructs Chapter 4 (Analisis dan Perancangan Sistem) for thesis scope."""
        subsections = [
            SubSectionOutline(
                id="4.1",
                title="Analisis Kebutuhan Sistem",
                focus_points=[
                    "Kebutuhan fungsional perangkat lunak berdasarkan proses bisnis statistik BPS",
                    "Kebutuhan non-fungsional (kinerja, konkurensi, keandalan, keamanan data mikro)",
                ],
                search_queries=["analisis kebutuhan fungsional non-fungsional"],
                estimated_paragraphs=2,
            ),
            SubSectionOutline(
                id="4.2",
                title="Perancangan Arsitektur dan Komponen Sistem",
                focus_points=[
                    "Diagram Use Case dan Activity Diagram proses bisnis utama",
                    "Skema basis data relasional/NoSQL dan kontrak antarmuka REST API",
                ],
                search_queries=["use case activity diagram perancangan database"],
                estimated_paragraphs=3,
            ),
            SubSectionOutline(
                id="4.3",
                title="Implementasi Komponen Artefak dan Algoritma",
                focus_points=[
                    "Implementasi logika bisnis backend dan algoritma komputasi inti",
                    "Strategi penanganan konkurensi dan proteksi kegagalan jaringan",
                ],
                search_queries=["implementasi algoritma backend"],
                estimated_paragraphs=3,
            ),
            SubSectionOutline(
                id="4.4",
                title="Hasil Pengujian dan Evaluasi Kualitas Perangkat Lunak",
                focus_points=[
                    "Hasil pengujian fungsionalitas (Blackbox Testing) dan metrik ISO/IEC 25010",
                    "Analisis latensi pemrosesan data dan akurasi model pada lingkungan simulasi",
                ],
                search_queries=["hasil pengujian blackbox ISO 25010 performa"],
                estimated_paragraphs=3,
            ),
        ]

        return ChapterOutline(
            id="bab_4",
            number=4,
            title="Analisis, Perancangan, dan Evaluasi Sistem",
            academic_goal="Mendemonstrasikan rekayasa artefak perangkat lunak dan melaporkan hasil pengujian empiris secara komprehensif.",
            subsections=subsections,
            estimated_words=2400,
        )

    def _build_chapter_5(self, topic: Dict[str, Any]) -> ChapterOutline:
        """Constructs Chapter 5 (Penutup) for thesis scope."""
        subsections = [
            SubSectionOutline(
                id="5.1",
                title="Kesimpulan",
                focus_points=[
                    "Sintesis pencapaian tujuan penelitian menjawab seluruh rumusan masalah",
                    "Ringkasan nilai kontribusi ilmiah dan performa artefak perangkat lunak yang dibangun",
                ],
                search_queries=["kesimpulan hasil penelitian"],
                estimated_paragraphs=2,
            ),
            SubSectionOutline(
                id="5.2",
                title="Saran & Pengembangan Lanjutan",
                focus_points=[
                    "Limitasi operasional sistem yang ditemukan saat evaluasi",
                    "Arahan riset masa depan (*future work*) untuk perbaikan artefak di lingkungan produksi BPS",
                ],
                search_queries=["saran penelitian selanjutnya future work"],
                estimated_paragraphs=2,
            ),
        ]

        return ChapterOutline(
            id="bab_5",
            number=5,
            title="Penutup",
            academic_goal="Menyimpulkan hasil rekayasa sistem dan memberikan arahan strategis bagi pengembangan riset selanjutnya.",
            subsections=subsections,
            estimated_words=1000,
        )
