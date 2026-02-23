# EVOLVE – Collaborative Annotation Infrastructure

## Overview

To enable secure collaborative annotation for the EVOLVE project, we deployed a private CVAT instance using Docker on a local machine and exposed it through a private Tailscale network.

This setup ensures:

- No public exposure of sensitive data
- Controlled access for collaborators
- Full reproducibility of the annotation environment
- Low infrastructure cost
- Fast deployment

---

## Architecture

```mermaid
flowchart LR
    subgraph Rina_Mac["Rina's Mac (Host Machine)"]
        Docker[Docker Engine]
        CVAT[CVAT Containers]
        Redis[Redis]
        DB[PostgreSQL DB]
        TS1[Tailscale Client]

        Docker --> CVAT
        Docker --> Redis
        Docker --> DB
        TS1 --> CVAT
    end

    subgraph AnneCamille_PC["Anne-Camille's PC"]
        TS2[Tailscale Client]
        Browser[Web Browser]
        TS2 --> Browser
    end

    TS2 <-- Private Mesh Network --> TS1
    ````

---

## Stack Components

1. Annotation Tool
   - CVAT (Computer Vision Annotation Tool)
   - Official repository: https://github.com/opencv/cvat
   - Deployed via Docker Compose
   - Runs locally on host machine

2. Containerization
   - Docker
   - Docker Compose
   - Persistent named volumes for data durability

3. Network Layer
   - Tailscale (private mesh VPN)
   - No public IP exposure
   - No router or firewall configuration required
   - Access restricted to authenticated devices within the private network

---

## Deployment steps

### 1. Install CVAT

```bash
git clone https://github.com/opencv/cvat ~/tools/cvat
cd ~/tools/cvat
docker compose up -d
```

Access locally

```
http://localhost:8080
```

Ensure CVAT listens on:

```
0.0.0.0
```

so that it is accessible from Tailscale.

### 2. Install Tailscale

On host machine:

```bash
brew install tailscale
tailscale up
tailscale ip -4
```

On collaborator machine:
- Install Tailscale
- Authenticate
- Join the same Tailscale network

Access CVAT remotely via:
```
http://<TAILSCALE_IP>:8080
```

---

## Backup Strategy

### Database Backup

CVAT PostgreSQL database can be backed up using:

```bash
docker exec -t cvat_db pg_dump -U root cvat > cvat_backup_YYYYMMDD.sql
```

This exports:
- Projects
- Tasks
- Jobs
- Users
- Annotations
- Metadata

Note: This does NOT include image files, which are stored in the Docker volume `cvat_cvat_data`.

---

## Security Considerations

- CVAT is not exposed to the public internet
- Access is restricted to authenticated Tailscale nodes
- Separate CVAT user accounts are created:
  - Admin (Rina)
  - Annotator (Anne-Camille)
- No sensitive dataset is publicly accessible

---

## Operational Constraints

- Host machine must remain powered on
- Stable internet connection required
- Docker containers must be running
- Tailscale must be active

If the host machine is offline, remote annotation is unavailable.

---

## Data Flow Integration with EVOLVE

CVAT is infrastructure-only and remains external to the EVOLVE repository.

Data flow:
1. Images prepared in `data/processed/images`
2. Uploaded to CVAT
3. Annotated collaboratively
4. Exported in YOLO format
5. Stored in `data/processed/labels`
6. Used for model training (`notebooks/02_training.ipynb`)

This separation ensures:
- Clean project structure
- Infrastructure independence
- Reproducibility
- Version control of training data only

---

## Rationale

This solution was selected because it:
- Ensures dataset privacy
- Avoids cloud hosting costs
- Enables real-time collaboration
- Maintains full control over data
- Demonstrates infrastructure competency in a machine learning workflow
- Separates infrastructure from experimentation

---

## Future Improvements

- Move deployment to NAS or dedicated mini-server
- Implement automated scheduled database backups
- Add annotation quality monitoring scripts
- Add inter-annotator agreement dashboard
- Version exported annotations via Git LFS
- Integrate CI checks on dataset consistency