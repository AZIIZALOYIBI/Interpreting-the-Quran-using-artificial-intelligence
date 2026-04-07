"use client";

import ErrorBoundary from "@/components/ErrorBoundary";
import AskQuranChat from "@/components/AskQuranChat";

/**
 * Wraps AskQuranChat inside an ErrorBoundary so that transient
 * rendering errors show a recoverable Arabic fallback UI instead of
 * crashing the whole page.
 */
export default function ChatWithBoundary() {
  return (
    <ErrorBoundary>
      <AskQuranChat />
    </ErrorBoundary>
  );
}
