import React, { useState } from "react";

type Result = {
    doc_id: string;
    score: number;
};

function App() {
    const [query, setQuery] = useState<string>("");
    const [results, setResults] = useState<Result[]>([]);
    const [loading, setLoading] = useState<boolean>(false);

    const handleSearch = async () => {
        if (!query.trim()) return;

        setLoading(true);

        try {
            const response = await fetch("http://localhost:5000/search", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ query })
            });

            const data: Result[] = await response.json();
            setResults(data);
        } catch (error) {
            console.error("Ошибка:", error);
        }

        setLoading(false);
    };

    return (
        <div style={styles.page}>
            <div style={styles.container}>
                <div style={styles.header}>
                    <h1 style={styles.title}>Поисковая система</h1>
                    <p style={styles.subtitle}>Найдите нужные документы за секунды</p>
                </div>

                <div style={styles.searchBox}>
                    <div style={styles.inputWrapper}>
                        <input
                            type="text"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Введите ваш запрос..."
                            style={styles.input}
                            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                        />
                    </div>

                    <button
                        onClick={handleSearch}
                        style={query.trim() ? styles.buttonActive : styles.button}
                        disabled={!query.trim()}
                    >
                        Найти
                    </button>
                </div>

                {loading && (
                    <div style={styles.loadingWrapper}>
                        <div style={styles.spinner}></div>
                        <p style={styles.loading}>Поиск...</p>
                    </div>
                )}

                <div style={styles.results}>
                    {results.length === 0 && !loading && (
                        <div style={styles.emptyState}>
                            <p style={styles.empty}>Нет результатов</p>
                            <p style={styles.emptySub}>Введите запрос для поиска</p>
                        </div>
                    )}

                    {results.length > 0 && !loading && (
                        <div style={styles.resultsHeader}>
                            <span style={styles.resultsCount}>Найдено: {results.length}</span>
                        </div>
                    )}

                    {results.map((res, index) => (
                        <div key={res.doc_id} style={styles.card}>
                            <div style={styles.cardNumber}>#{index + 1}</div>
                            <div style={styles.cardContent}>
                                <div style={styles.cardTitle}>
                                    Документ {res.doc_id}
                                </div>
                                <div style={styles.scoreWrapper}>
                                    <div style={styles.scoreBar}>
                                        <div style={{ width: `${res.score * 100}%`, ...styles.scoreFill }} />
                                    </div>
                                    <div style={styles.scoreText}>
                                        Сходство: {(res.score * 100).toFixed(1)}%
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default App;

const styles: { [key: string]: React.CSSProperties } = {
    page: {
        minHeight: "100vh",
        background: "linear-gradient(145deg, #f3f0ff 0%, #eef2ff 100%)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif",
        padding: "20px"
    },

    container: {
        background: "#ffffff",
        padding: "48px",
        borderRadius: "28px",
        width: "680px",
        maxWidth: "100%",
        boxShadow: "0 20px 35px -10px rgba(0, 0, 0, 0.05), 0 0 0 1px rgba(0, 0, 0, 0.02)",
        transition: "all 0.2s ease"
    },

    header: {
        textAlign: "center",
        marginBottom: "40px"
    },

    title: {
        fontSize: "34px",
        fontWeight: "600",
        color: "#2d2b4e",
        marginBottom: "10px",
        letterSpacing: "-0.3px"
    },

    subtitle: {
        color: "#9ca3af",
        fontSize: "15px",
        fontWeight: "400"
    },

    searchBox: {
        display: "flex",
        gap: "12px",
        marginBottom: "32px"
    },

    inputWrapper: {
        flex: 1
    },

    input: {
        width: "100%",
        padding: "14px 18px",
        borderRadius: "20px",
        border: "1.5px solid #edeef2",
        fontSize: "15px",
        backgroundColor: "#fefefe",
        transition: "all 0.2s ease",
        outline: "none",
        fontFamily: "inherit",
        color: "#1f1f2e",
        boxSizing: "border-box"
    },

    button: {
        padding: "14px 28px",
        borderRadius: "20px",
        border: "none",
        background: "#edeef2",
        color: "#a1a1aa",
        cursor: "not-allowed",
        fontWeight: "500",
        fontSize: "15px",
        transition: "all 0.2s ease",
        fontFamily: "inherit"
    },

    buttonActive: {
        padding: "14px 28px",
        borderRadius: "20px",
        border: "none",
        background: "#8b7bd9",
        color: "white",
        cursor: "pointer",
        fontWeight: "500",
        fontSize: "15px",
        transition: "all 0.2s ease",
        fontFamily: "inherit",
        boxShadow: "0 2px 8px rgba(139, 123, 217, 0.2)"
    },

    loadingWrapper: {
        textAlign: "center",
        padding: "40px 0"
    },

    spinner: {
        width: "36px",
        height: "36px",
        margin: "0 auto 14px",
        border: "3px solid #edeef2",
        borderTop: "3px solid #8b7bd9",
        borderRadius: "50%",
        animation: "spin 0.7s linear infinite"
    },

    loading: {
        color: "#8b7bd9",
        fontSize: "14px",
        margin: 0,
        fontWeight: "500"
    },

    results: {
        marginTop: "8px"
    },

    resultsHeader: {
        marginBottom: "18px",
        paddingBottom: "10px",
        borderBottom: "1px solid #f0f0f4"
    },

    resultsCount: {
        fontSize: "13px",
        fontWeight: "500",
        color: "#8b7bd9",
        textTransform: "uppercase",
        letterSpacing: "0.4px"
    },

    emptyState: {
        textAlign: "center",
        padding: "50px 20px"
    },

    empty: {
        color: "#cbcbd4",
        fontSize: "16px",
        margin: "0 0 8px 0",
        fontWeight: "500"
    },

    emptySub: {
        color: "#e2e2e8",
        fontSize: "13px",
        margin: 0
    },

    card: {
        display: "flex",
        alignItems: "center",
        gap: "16px",
        padding: "18px",
        borderRadius: "20px",
        background: "#fafaff",
        marginBottom: "12px",
        transition: "all 0.2s ease",
        cursor: "pointer",
        border: "1px solid #f1f1f6"
    },

    cardNumber: {
        fontSize: "22px",
        fontWeight: "600",
        color: "#dcdce8",
        minWidth: "44px",
        textAlign: "center"
    },

    cardContent: {
        flex: 1
    },

    cardTitle: {
        fontWeight: "500",
        fontSize: "15px",
        marginBottom: "12px",
        color: "#2d2b4e"
    },

    scoreWrapper: {
        display: "flex",
        alignItems: "center",
        gap: "12px"
    },

    scoreBar: {
        flex: 1,
        height: "5px",
        backgroundColor: "#e9e9f0",
        borderRadius: "3px",
        overflow: "hidden"
    },

    scoreFill: {
        height: "100%",
        background: "linear-gradient(90deg, #8b7bd9, #b4a7ff)",
        borderRadius: "3px",
        transition: "width 0.3s ease"
    },

    scoreText: {
        fontSize: "12px",
        fontWeight: "500",
        color: "#8b7bd9",
        minWidth: "100px",
        textAlign: "right"
    }
};

// Анимация для спиннера
const styleSheet = document.createElement("style");
styleSheet.textContent = `
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    input:focus {
        border-color: #b4a7ff;
        box-shadow: 0 0 0 3px rgba(139, 123, 217, 0.08);
    }
    
    button:hover:enabled {
        transform: translateY(-1px);
        background: #7c6bc9;
        box-shadow: 0 4px 12px rgba(139, 123, 217, 0.25);
    }
    
    div[style*="card"]:hover {
        transform: translateX(3px);
        border-color: #e5dfff;
        background: #ffffff;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    }
`;
document.head.appendChild(styleSheet);