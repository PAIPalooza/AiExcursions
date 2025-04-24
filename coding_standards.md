# 📋 GeoVoyager Coding Standards

Based on Semantic Seed Coding Standards V2.0, adapted for our location-based, real-time application.

## 🔄 Git Workflow

### Branch Naming
```
feature/POI-{id}    # For POI management features
feature/VOICE-{id}  # For audio/voice features
feature/GROUP-{id}  # For group sync features
bug/BUG-{id}       # For bug fixes
chore/INF-{id}     # For infrastructure work
```

### Commit Messages
```
feat(poi): add geofence radius validation
feat(voice): implement AWS S3 audio streaming
fix(group): resolve realtime sync delay
chore(deps): update FastAPI to 0.100.0
```

## 🧪 Testing Standards

### FastAPI Backend Tests
```python
# Example POI Test Pattern
def test_poi_geofence_match():
    """BDD: Given a user location within 20m of POI
       When checking for nearby POIs
       Then the POI should be included in results"""
    assert check_poi_proximity(user_loc, poi_loc) == True
```

### React Frontend Tests
```javascript
// Example Group Sync Test Pattern
describe('GroupSession', () => {
  it('should sync POI state across participants', async () => {
    // Given a group session with 2 participants
    // When leader moves to new POI
    // Then follower should receive update within 500ms
  });
});
```

## 🏗️ Code Organization

### FastAPI Backend Structure
```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── pois.py
│   │   │   ├── tours.py
│   │   │   └── groups.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── models/
│   │   └── domain/
│   └── services/
└── tests/
```

### React Frontend Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── map/
│   │   ├── audio/
│   │   └── group/
│   ├── hooks/
│   │   ├── useGeolocation.ts
│   │   └── useAudioPlayback.ts
│   └── services/
└── tests/
```

## 📝 Code Style Guidelines

### Python (Backend)
- Use type hints for all function parameters and returns
- Use Pydantic models for all API requests/responses
- Maximum line length: 88 characters (Black formatter)
- Docstring format: Google style

```python
from pydantic import BaseModel
from typing import List, Optional

class POICreate(BaseModel):
    """Point of Interest creation model.
    
    Attributes:
        title: Display name of the POI
        latitude: GPS latitude coordinate
        longitude: GPS longitude coordinate
        audio_url: Optional S3 URL for narration
    """
    title: str
    latitude: float
    longitude: float
    audio_url: Optional[str] = None
```

### TypeScript (Frontend)
- Use TypeScript for all new components
- Use functional components with hooks
- Props interfaces must be explicitly defined
- Use CSS-in-JS with Tailwind

```typescript
interface POIMarkerProps {
  latitude: number;
  longitude: number;
  isActive: boolean;
  onEnterGeofence: () => void;
}

const POIMarker: React.FC<POIMarkerProps> = ({
  latitude,
  longitude,
  isActive,
  onEnterGeofence,
}) => {
  // Implementation
};
```

## 🔐 Security Standards

### API Security
- All endpoints must validate Supabase JWT
- S3 uploads must use pre-signed URLs
- Geolocation data must be GDPR compliant
- Rate limiting on all public endpoints

### Frontend Security
- No sensitive data in localStorage
- Sanitize all location data before display
- Clear session data on logout
- Use environment variables for all configs

## 📊 Performance Standards

### Backend Metrics
- API response time < 200ms
- Geofence calculation < 50ms
- Group sync latency < 500ms
- 99.9% uptime SLA

### Frontend Metrics
- First Contentful Paint < 1.5s
- Time to Interactive < 3.5s
- GPS polling interval: 5s
- Audio start latency < 100ms

## 🔄 CI/CD Requirements

### Pre-merge Checks
- All tests must pass
- Coverage > 80%
- No TypeScript errors
- ESLint/Black formatting
- Security scan clean

### Deployment Checks
- Database migration validation
- S3 bucket accessibility
- Supabase connection test
- GPS permission check
- Audio codec validation

## 📝 Documentation Requirements

### API Documentation
- OpenAPI/Swagger for all endpoints
- Example requests/responses
- Rate limit documentation
- Error code explanations

### Component Documentation
- Storybook for UI components
- GPS accuracy requirements
- Audio format specifications
- Group sync limitations
