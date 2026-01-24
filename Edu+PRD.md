
# Edu+ PRD

A specialized scheduling utility for IB (International Baccalaureate) students designed to transform complex, institutional JSON data into clean, personalized, and syncable digital schedules.

**Experience Qualities**:

1. **Clarity** - Eliminates visual noise by filtering global grade-level data down to the individual student level.
2. **Precision** - Leverages structured JSON data to ensure 100% accuracy in class times and locations.
3. **Versatility** - Provides both a static visual reference (Photo) and a dynamic calendar integration (.ics).

**Complexity Level**: Mid-Tier Utility
This application manages the transformation of structured JSON objects into filtered user models. It requires logic for group-based filtering (Homeroom) and data conversion for calendar protocols.

---

## Essential Features

### 1. Smart Data Ingestion (JSON)

* **Functionality**: The app parses a master JSON file containing all classes, teachers, and rooms for a specific grade or school year.
* **Structure**: It maps `subject_id`, `time_slots`, and `group_tags` (e.g., "11-C" or "Standard Level Biology").
* **Purpose**: Replaces the error-prone OCR process with a direct, "source of truth" data stream.
* **Success criteria**: Zero data loss during ingestion; ability to handle nested JSON objects for overlapping elective blocks.

### 2. Two-Step Personalized Selection

* **Step A: Homeroom Selection**: User first selects their primary class group (e.g., "Grade 11-A"). This instantly filters out all non-applicable core classes.
* **Step B: Elective Picking**: Based on the remaining data, the user checks their specific electives (e.g., "Physics HL," "Economics SL").
* **Logic**: The app cross-references the user's choices against the master JSON to build a "Personal Profile" model.
* **Success criteria**: The UI must dynamically update the elective list based on the chosen Homeroom.

### 3. Multi-Format Export (Visual & Calendar)

* **Photo Export (.png)**:
* Generates a high-legibility grid with **Academic Indigo** accents.
* Optimized for mobile lock screens (9:16 aspect ratio).


* **Apple Calendar Export (.ics)**:
* Converts the filtered JSON data into the `iCalendar` format.
* Includes "Subject Name" as the title and "Room Number" as the location.


* **Purpose**: Allows students to choose between a "glanceable" photo or a "functional" system notification.

### 4. Style & Dark Mode Customization

* **Functionality**: Users can toggle between "Light" and "OLED Dark" modes before exporting.
* **Wallpaper Preset**: Automatically pads the image so that the clock on an iPhone lock screen doesn't overlap with the first period.

---

## Technical Workflow

1. **Load**: Website fetches/loads the master JSON timetable.
2. **Filter**: User selects **Homeroom**  App narrows down the list of potential classes.
3. **Select**: User selects **Electives**  App creates a unique student schedule object.
4. **Render/Compile**:
* **Image Path**: Canvas API draws the grid based on the object.
* **Calendar Path**: A script generates a `.ics` blob for download.



---

## Design Direction

The UI should feel like a premium, native Apple application.

* **Primary Color**: Academic Indigo `oklch(0.40 0.12 260)`
* **Accent Color**: Mint Green `oklch(0.85 0.12 160)`
* **Typography**:
* **Inter**: For navigation and labels.
* **IBM Plex Mono**: For time codes (e.g., `08:30 - 09:25`) to ensure tabular alignment.



### Home Screen Layout (Mobile-First)

1. **Welcome Header**: "Build your Edu+ Schedule."
2. **Homeroom Dropdown**: Large, accessible selector.
3. **Elective Grid**: A list of toggleable cards for subjects.
4. **Action Bar**: Two distinct buttons: `[ Save to Photos ]` and `[ Add to Calendar ]`.

---

## Success Metrics

* **Accuracy**: The `.ics` file reflects the exact start/end times provided in the JSON.
* **Efficiency**: A user can go from "Open Site" to "Calendar Export" in under 30 seconds.
* **Legibility**: The exported photo must be readable at 50% brightness on a mobile device.