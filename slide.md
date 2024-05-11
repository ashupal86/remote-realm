# Backend Diagram
```mermaid
graph TD
    A[Backend] -->|Handles Logic| B[Game Logic]
    A -->|Manages Data| C[Database]
    A -->|Communicates| D[Networking]
```

```mermaid
graph TD
    A[Frontend] -->|User Interface| B[UI Design]
    A -->|Real-time Updates| C[Socket.IO]
    A -->|Interactive| D[User Interaction]
  ```

  ```mermaid
  graph TD
    A[Database] -->|User Information| B[User Data]
    A -->|Game State| C[Game Data]
    A -->|Role Assignment| D[Roles]
```

``` mermaid
graph TD
    A[Networking] -->|WebSockets| B[Web Communication]
    A -->|Client-Server| C[Communication]
    A -->|Real-time| D[Updates]
```

```mermaid
graph TD
    A[User Interaction] -->|Role Selection| B[Choose Roles]
    A -->|Room Joining| C[Join Rooms]
    A -->|Code Entry| D[Enter Room Code]
```
```mermaid
graph TD
    A[Role Assignment] -->|Random Assignment| B[Assign Roles]
    A -->|King, Minister, Soldier, Thief| C[Roles]
    A -->|Objective Setting| D[Define Objectives]
```

```mermaid
graph TD
    A[Project Overview] -->|Multiplayer Game| B[Game Concept]
    A -->|Role Dynamics| C[Role Assignment]
    A -->|Technology Stack| D[Technologies Used]
    A -->|Game Flow| E[Player Interactions]
  ```

  ```mermaid
  
graph LR
    A[Client] -->|Socket.IO| B[Frontend Server]
    B -->|Flask-SocketIO| C[Backend Server]
```