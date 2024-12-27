# Memory Cleanup Protocol

## Core Purpose [1000]
- **Process** two data collections:
  - _Conversation history of AI agent_
  - _Raw memories from vector database (similarity score based)_
- **Filter** relevant memories
- **Remove** irrelevant database entries
- **Focus** on current conversation context

## Implementation Rules [2000]

### Processing Guidelines
- **Review** conversation history focus
- **Analyze** end of conversation for current topic
- **Remove** unrelated database results
- **Retain** relevant and helpful memories
- **Validate** memory relevance

### Memory Evaluation
- **Relevance**: _Topic alignment check_
- **Usefulness**: _Future conversation value_
- **Context**: _Current discussion applicability_
- **Quality**: _Information accuracy and completeness_

## Output Format [3000]

### Relevant Memories Found
```markdown
1. Guide how to create a web app including code
2. Javascript snippets from snake game development
3. SVG image generation for game sprites with examples

Check your knowledge_tool for more details.

No Relevant Memories
No relevant memories on the topic found.

## System References

- Technical Solutions: [1100-1500]
- Process Solutions: [2100-2500]
- Problem Resolution: [3100-3500]
- Best Practices: [4100-4500]