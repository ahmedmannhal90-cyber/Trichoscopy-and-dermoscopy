exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return {
      statusCode: 405,
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ error: { message: "Method not allowed" } }),
    };
  }
  try {
    const body = JSON.parse(event.body);

    // Resize images to reduce payload size
    const messages = body.messages.map(msg => {
      if (Array.isArray(msg.content)) {
        return {
          ...msg,
          content: msg.content.map(block => {
            if (block.type === "image") {
              return {
                ...block,
                source: {
                  ...block.source,
                  data: block.source.data.substring(0, 500000)
                }
              };
            }
            return block;
          })
        };
      }
      return msg;
    });

    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": "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",
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-haiku-4-5",
        max_tokens: 1500,
        messages: messages,
      }),
    });

    const text = await response.text();
    return {
      statusCode: 200,
      headers: { "Access-Control-Allow-Origin": "*", "Content-Type": "application/json" },
      body: text,
    };
  } catch (err) {
    return {
      statusCode: 500,
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ error: { message: err.message } }),
    };
  }
};
