# Database Schema Design

## Task 1: Public Health Database

### Entity-Relationship Model

#### Entities

1. **Country**
   - country_id (PK)
   - country_name
   - region
   - population

2. **VaccinationRecord**
   - record_id (PK)
   - country_id (FK)
   - date
   - vaccine_type
   - doses_administered
   - population_vaccinated
   - percentage_vaccinated

3. **DiseaseOutbreak**
   - outbreak_id (PK)
   - country_id (FK)
   - disease_name
   - date_reported
   - cases_reported
   - deaths_reported
   - recovery_rate

### Relationships
- Country 1:N VaccinationRecord
- Country 1:N DiseaseOutbreak

### SQL Schema

```sql
CREATE TABLE IF NOT EXISTS country (
    country_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_name TEXT NOT NULL UNIQUE,
    region TEXT,
    population INTEGER
);

CREATE TABLE IF NOT EXISTS vaccination_record (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    vaccine_type TEXT,
    doses_administered INTEGER,
    population_vaccinated INTEGER,
    percentage_vaccinated REAL,
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);

CREATE TABLE IF NOT EXISTS disease_outbreak (
    outbreak_id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id INTEGER NOT NULL,
    disease_name TEXT NOT NULL,
    date_reported TEXT NOT NULL,
    cases_reported INTEGER,
    deaths_reported INTEGER,
    recovery_rate REAL,
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);

CREATE INDEX idx_vaccination_date ON vaccination_record(date);
CREATE INDEX idx_outbreak_date ON disease_outbreak(date_reported);
CREATE INDEX idx_country_name ON country(country_name);
```
```