"""
Design a version history system for a single document (like Google Docs' version history).

You need to support:

edit(content) — save a new version of the document with the given full content, becomes the new "current" version
get_current() — return the current version's content
undo() — revert to the previous version
redo() — if you've undone, move forward again to the version you undid
restore_version(version_id) — jump directly to a specific past version by its ID (not just one step back/forward), and this becomes the new current version going forward

The core structure is a linear history (versions in order), but restore_version is the twist: once you jump to an arbitrary past version and then make a new edit(), what happens to the versions that came after the one you restored to? Do they get discarded, or does history branch? That's a real design decision, not just an implementation detail — think about what a user would actually expect from "Google Docs" behavior here.
"""