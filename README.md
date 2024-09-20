```
graph TD
    A[Client Browser] -->|HTTP Requests| B[React Frontend]
    B <-->|API Calls| C[Flask Backend]
    C --> D[Recommendation Engine]
    D --> E[(Pickle File)]
    C --> F[(Book Database)]
    G[Kaggle Dataset] -->|Train| H[Hybrid Recommender Model]
    H -->|Export| E
    
    subgraph Frontend
    B
    end
    
    subgraph Backend
    C
    D
    E
    F
    end
    
    subgraph Model Training
    G
    H
    end

    classDef browser fill:#e1f5fe,stroke:#01579b;
    classDef frontend fill:#e8f5e9,stroke:#2e7d32;
    classDef backend fill:#fff3e0,stroke:#e65100;
    classDef database fill:#f3e5f5,stroke:#4a148c;
    classDef training fill:#fffde7,stroke:#f57f17;

    class A browser
    class B frontend
    class C,D backend
    class E,F database
    class G,H training
```