flowchart TD
    A([User Preferences]) --> B

    subgraph INPUT["INPUT"]
        A
        A1["favorite_mood\ntarget_energy\ntarget_valence\ntarget_acoustic"]
        A --> A1
    end

    A1 --> B

    subgraph PROCESS["THE LOOP — Score Every Song in songs.csv"]
        B["Load songs.csv\nload_songs()"] --> C["For each song..."]

        C --> R1["Rule 1: Mood Match\nweight × 0.45\n─────────────\nExact match → 1.0\nAdjacent mood → 0.5\nNo match → 0.0"]
        C --> R2["Rule 2: Energy Proximity\nweight × 0.40\n─────────────\n1.0 − |target_energy − song.energy|"]
        C --> R3["Rule 3: Valence Alignment\nbonus +0.1\n─────────────\nPositive mood + valence > 0.7 ✓\nDark mood + valence < 0.6 ✓"]
        C --> R4["Rule 4: Danceability Boost\nbonus up to +0.1\n─────────────\nOnly applies if\ntarget_energy > 0.7"]

        R1 --> S["Final Score\n────────────────────────────────\n(mood × 0.45) + (energy × 0.40)\n+ valence_bonus + dance_bonus"]
        R2 --> S
        R3 --> S
        R4 --> S

        S --> E["Build Explanation String\nmood_reason + energy_reason\n+ valence_reason"]
    end

    E --> F

    subgraph OUTPUT["OUTPUT — Top K Recommendations"]
        F["Sort all songs by score\n(highest → lowest)"]
        F --> G["Return Top K songs\nwith score + explanation"]
        G --> H(["Ranked Results\n#1 Best Match\n#2\n#3\n..."])
    end

    style INPUT fill:#1e3a5f,color:#ffffff,stroke:#4a90d9
    style PROCESS fill:#2d1b4e,color:#ffffff,stroke:#9b59b6
    style OUTPUT fill:#1a4a2e,color:#ffffff,stroke:#2ecc71
    style R1 fill:#3b1f6b,color:#ffffff,stroke:#9b59b6
    style R2 fill:#3b1f6b,color:#ffffff,stroke:#9b59b6
    style R3 fill:#3b1f6b,color:#ffffff,stroke:#9b59b6
    style R4 fill:#3b1f6b,color:#ffffff,stroke:#9b59b6
    style S fill:#4a2080,color:#ffffff,stroke:#c39bd3
    style A fill:#1a3a6b,color:#ffffff,stroke:#4a90d9
    style H fill:#1a5c38,color:#ffffff,stroke:#2ecc71
flowchart TD
    A([User Preferences]) --> B

    subgraph INPUT["INPUT"]
        A
        A1["favorite_mood\ntarget_energy\ntarget_valence\ntarget_acoustic"]
        A --> A1
    end

    A1 --> B

    subgraph PROCESS["THE LOOP — Score Every Song in songs.csv"]
        B["Load songs.csv\nload_songs()"] --> C["For each song..."]

        C --> R1["Rule 1: Mood Match\nweight × 0.45\n─────────────\nExact match → 1.0\nAdjacent mood → 0.5\nNo match → 0.0"]
        C --> R2["Rule 2: Energy Proximity\nweight × 0.40\n─────────────\n1.0 − |target_energy − song.energy|"]
        C --> R3["Rule 3: Valence Alignment\nbonus +0.1\n─────────────\nPositive mood + valence > 0.7 ✓\nDark mood + valence < 0.6 ✓"]
        C --> R4["Rule 4: Danceability Boost\nbonus up to +0.1\n─────────────\nOnly applies if\ntarget_energy > 0.7"]

        R1 --> S["Final Score\n────────────────────────────────\n(mood × 0.45) + (energy × 0.40)\n+ valence_bonus + dance_bonus"]
        R2 --> S
        R3 --> S
        R4 --> S

        S --> E["Build Explanation String\nmood_reason + energy_reason\n+ valence_reason"]
    end

    E --> F

    subgraph OUTPUT["OUTPUT — Top K Recommendations"]
        F["Sort all songs by score\n(highest → lowest)"]
        F --> G["Return Top K songs\nwith score + explanation"]
        G --> H(["Ranked Results\n#1 Best Match\n#2\n#3\n..."])
    end

    style INPUT fill:#1e3a5f,color:#ffffff,stroke:#4a90d9
    style PROCESS fill:#2d1b4e,color:#ffffff,stroke:#9b59b6
    style OUTPUT fill:#1a4a2e,color:#ffffff,stroke:#2ecc71
    style R1 fill:#3b1f6b,color:#ffffff,stroke:#9b59b6
    style R2 fill:#3b1f6b,color:#ffffff,stroke:#9b59b6
    style R3 fill:#3b1f6b,color:#ffffff,stroke:#9b59b6
    style R4 fill:#3b1f6b,color:#ffffff,stroke:#9b59b6
    style S fill:#4a2080,color:#ffffff,stroke:#c39bd3
    style A fill:#1a3a6b,color:#ffffff,stroke:#4a90d9
    style H fill:#1a5c38,color:#ffffff,stroke:#2ecc71
