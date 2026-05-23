import phoenix as px
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from openinference.instrumentation.langchain import LangChainInstrumentor
import time

_telemetry_store = {
    "traces": [],
    "tool_calls": {"search_properties": 0, "calculate_roi": 0, "get_locality_insights": 0, "rag_search": 0},
    "rag_retrievals": 0,
    "gemini_calls": 0,
    "total_latency_ms": 0
}

def initialize_telemetry():
    """
    Initializes telemetry:
    1. Launches local Arize Phoenix session using px.launch_app().
    2. Sets up TracerProvider and OTLP HTTP SpanExporter pointing to the Phoenix collector endpoint.
    3. Instruments LangChain callbacks.
    """
    endpoint = "http://localhost:6006/v1/traces"
    try:
        session = px.launch_app()
        if session and hasattr(session, "url"):
            endpoint = f"{session.url}/v1/traces"
            print(f"============================================================")
            print(f"Arize Phoenix observability dashboard launched at: {session.url}")
            print(f"OTLP Collector endpoint: {endpoint}")
            print(f"============================================================")
    except Exception as e:
        print(f"Phoenix app launch ignored or failed (might be already running): {e}")

    try:
        # Prevent double registration of provider
        provider = TracerProvider()
        exporter = OTLPSpanExporter(endpoint=endpoint)
        processor = SimpleSpanProcessor(exporter)
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        
        # Instrument LangChain
        LangChainInstrumentor().instrument()
        print("LangChain OpenTelemetry Instrumentation successfully registered.")
    except Exception as e:
        print(f"Error during OpenTelemetry initialization/instrumentation: {e}")

def log_tool_call(tool: str = None, inputs: dict = None, output_summary: str = None, latency_ms: int = None, tool_name: str = None, outputs: str = None):
    """
    Logs a tool call execution details.
    """
    t_name = tool or tool_name or "unknown_tool"
    detail = output_summary or outputs or ""
    lat = latency_ms or 0
    
    # Increment tool-specific counters
    if t_name in _telemetry_store["tool_calls"]:
        _telemetry_store["tool_calls"][t_name] += 1
    else:
        _telemetry_store["tool_calls"][t_name] = 1
    
    # Update total latency
    _telemetry_store["total_latency_ms"] += lat
    
    # Append trace log
    _telemetry_store["traces"].append({
        "timestamp": time.strftime("%H:%M:%S"),
        "name": t_name,
        "detail": f"Inputs: {inputs} | Output: {detail}",
        "latency": lat
    })

def log_rag_retrieval(query: str, num_results: int, top_result_preview: str, latency_ms: int = 0):
    """
    Logs a RAG retrieval execution details.
    """
    # Increment counter
    _telemetry_store["rag_retrievals"] += 1
    
    # Also track it under tool_calls if required
    if "rag_search" in _telemetry_store["tool_calls"]:
        _telemetry_store["tool_calls"]["rag_search"] += 1
    
    # Update total latency
    _telemetry_store["total_latency_ms"] += latency_ms
    
    # Append trace log
    _telemetry_store["traces"].append({
        "timestamp": time.strftime("%H:%M:%S"),
        "name": "rag_search",
        "detail": f"Query: '{query}' | Results: {num_results} | Top Preview: '{top_result_preview}'",
        "latency": latency_ms
    })

def log_gemini_call(prompt_tokens: int, response_tokens: int, latency_ms: int):
    """
    Logs a Gemini model invocation execution details.
    """
    # Increment counter
    _telemetry_store["gemini_calls"] += 1
    
    # Update total latency
    _telemetry_store["total_latency_ms"] += latency_ms
    
    # Append trace log
    _telemetry_store["traces"].append({
        "timestamp": time.strftime("%H:%M:%S"),
        "name": "gemini_inference",
        "detail": f"Prompt Tokens: {prompt_tokens} | Response Tokens: {response_tokens}",
        "latency": latency_ms
    })

def get_telemetry_summary() -> dict:
    """
    Returns the accumulated telemetry data structure matching the frontend expectations.
    """
    return {
        "total_latency_ms": _telemetry_store["total_latency_ms"],
        "tool_calls": {
            "search_properties": _telemetry_store["tool_calls"].get("search_properties", 0),
            "calculate_roi": _telemetry_store["tool_calls"].get("calculate_roi", 0),
            "get_locality_insights": _telemetry_store["tool_calls"].get("get_locality_insights", 0),
            "rag_search": _telemetry_store["tool_calls"].get("rag_search", 0)
        },
        "rag_retrievals": _telemetry_store["rag_retrievals"],
        "gemini_calls": _telemetry_store["gemini_calls"],
        "traces": _telemetry_store["traces"]
    }
