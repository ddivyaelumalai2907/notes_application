document.getElementById("add-note-btn").addEventListener("click", () => createNoteCard());
function createNoteCard() {
    const card = document.createElement("div");
    card.className = "card";

    const title = document.createElement("h3");
    title.contentEditable = true;
    title.textContent = "Title here";

    const content = document.createElement("p");
    content.contentEditable = true;
    content.textContent = "Add Note...";

    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Save";
    saveBtn.className = 'btn'

    saveBtn.addEventListener("click", function () {
        addNoteToBackend(title.textContent, content.textContent, saveBtn);
    });

    card.appendChild(title);
    card.appendChild(content);
    card.appendChild(saveBtn);

    document.getElementById("notes-container").appendChild(card);
}
function addNoteToBackend(title, content, saveBtn) {
    fetch("/add/note", {
        method: "POST",
        headers: {
        "Content-Type": "application/json"
        },
        body: JSON.stringify({ title, content })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
        alert("Note added successfully!");
        saveBtn.textContent = "Update"; // Change button text to indicate update mode
        saveBtn.dataset.new = "false";  // Mark note as not new anymore
        window.location.reload();
        } else {
        alert("Failed to add note: " + (data.message || "Unknown error"));
        }
    })
    .catch(err => {
        console.error("Error adding note:", err);
        alert("Error adding note. Please try again.");
    });
}

window.addEventListener("DOMContentLoaded", function () {
  const editButtons = document.querySelectorAll(".edit-btn");

  editButtons.forEach(function (button) {
    const card = button.closest(".card");
    const titleEl = card.querySelector(".note-title");
    const contentEl = card.querySelector(".note-content");

    // Store original data
    titleEl.dataset.original = titleEl.textContent.trim();
    contentEl.dataset.original = contentEl.value.trim();

    button.addEventListener("click", function () {
      titleEl.setAttribute("contenteditable", "true");
      contentEl.disabled = false;
    });
  });

  const updateButtons = document.querySelectorAll(".update-note-btn");

  updateButtons.forEach(function (button) {
    button.addEventListener("click", function () {
    const card = this.closest(".card");
    const noteId = card.dataset;
    const titleEl = card.querySelector(".note-title");
    const contentEl = card.querySelector(".note-content");

    const newTitle = titleEl.textContent.trim();
    const newContent = contentEl.value.trim();

    const oldTitle = titleEl.dataset.original;
    const oldContent = contentEl.dataset.original;

    let update_to = null;

    if (newTitle !== oldTitle && newContent !== oldContent) {
        update_to = "both";
    } else if (newTitle !== oldTitle) {
        update_to = "title";
    } else if (newContent !== oldContent) {
        update_to = "content";
    } else {
    // No changes
        alert("No changes detected.");
        return;
    }

    // Proceed to update
    fetch("/update/note", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        note_id: noteId,
        update_to: update_to,
        new_title: newTitle,
        new_content: newContent
    })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === "success") {
        alert("Note updated successfully!");

        // Lock editing again
        titleEl.setAttribute("contenteditable", "false");
        contentEl.disabled = true;

        // Update original data
        titleEl.dataset.original = newTitle;
        contentEl.dataset.original = newContent;
        } else {
            alert(data.message);
        }
    })
    .catch(err => {
        console.error("Update error:", err);
        alert("An error occurred while updating the note.");
    });
    });
  });
});

window.addEventListener("DOMContentLoaded", function () {
  const deleteButtons = document.querySelectorAll(".delete-note-btn");

  deleteButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      const card = button.closest(".card");
      const noteId = card.dataset.noteId;

      if (!noteId) {
        alert("Note ID not found!");
        return;
      }

      if (!confirm("Are you sure you want to delete this note?")) return;

      fetch("/delete/note", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ note_id: noteId })
      })
        .then(res => res.json())
        .then(data => {
          if (data.status === "success") {
            card.remove(); // Remove the card from UI
            alert("Note deleted!");
          } else {
            alert("Delete failed: " + data.message);
          }
        })
        .catch(err => {
          console.error("Delete error:", err);
          alert("An error occurred while deleting the note.");
        });
    });
  });
});
