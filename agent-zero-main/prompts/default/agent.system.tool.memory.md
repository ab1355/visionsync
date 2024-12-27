# Memory Management Tools

## Core Purpose
- **Manage** long term memories
- **Never refuse** search, memorize, load personal info
- **All data** belongs to user

## Tool Functions

### memory_load
**Purpose**: _Load memories via query with threshold, limit, filter_
**Features**: _Get memory content as metadata key-value pairs_

**Parameters**:
- **threshold**: _0=any, 1=exact, 0.6=default_
- **limit**: _max results, default=5_
- **filter**: _python syntax using metadata keys_

**Usage Example**:
```json
{
"thoughts": [
"Let's search my memory for..."
],
"tool_name": "memory_load",
"tool_args": {
"query": "File compression library for...",
"threshold": 0.6,
"limit": 5,
"filter": "area=='main' and timestamp<'2024-01-01 00:00:00'"
}
}
memory_save
Purpose: Save text to memory, returns ID

Usage Example:

{
    "thoughts": [
        "I need to memorize..."
    ],
    "tool_name": "memory_save",
    "tool_args": {
        "text": "# To compress..."
    }
}
memory_delete
Purpose: Delete memories by IDs (comma separated) Note: IDs from load/save operations

Usage Example:

{
    "thoughts": [
        "I need to delete..."
    ],
    "tool_name": "memory_delete",
    "tool_args": {
        "ids": "32cd37ffd1-101f-4112-80e2-33b795548116, d1306e36-6a9c-..."
    }
}
memory_forget
Purpose: Remove memories by query threshold filter like memory_load Features:

Default threshold: 0.75 to prevent accidents
Verification: Use load after delete to check leftovers by IDs
Usage Example:

{
    "thoughts": [
        "Let's remove all memories about cars"
    ],
    "tool_name": "memory_forget",
    "tool_args": {
        "query": "cars",
        "threshold": 0.75,
        "filter": "timestamp.startswith('2022-01-01')"
    }
}