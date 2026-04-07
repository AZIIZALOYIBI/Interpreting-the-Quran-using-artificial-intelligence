"use client";

import React, { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  errorMessage: string;
}

/**
 * React Error Boundary — catches runtime errors in the component tree
 * and displays a localised Arabic fallback UI instead of a blank page.
 */
export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, errorMessage: "" };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, errorMessage: error.message };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    // In production you would forward this to an error-tracking service
    console.error("ErrorBoundary caught an error:", error, info.componentStack);
  }

  private handleReset = (): void => {
    this.setState({ hasError: false, errorMessage: "" });
  };

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div
          dir="rtl"
          className="flex flex-col items-center justify-center min-h-[300px] p-8 text-center bg-red-50 rounded-2xl border border-red-200"
        >
          <div className="text-5xl mb-4">⚠️</div>
          <h2 className="text-xl font-bold text-red-800 mb-2">
            حدث خطأ غير متوقع
          </h2>
          <p className="text-red-600 text-sm mb-6 max-w-md">
            عذراً، واجه هذا الجزء من الصفحة مشكلة تقنية. يمكنك المحاولة مجدداً
            أو إعادة تحميل الصفحة.
          </p>
          <div className="flex gap-3">
            <button
              onClick={this.handleReset}
              className="px-5 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-medium transition-colors"
            >
              حاول مجدداً
            </button>
            <button
              onClick={() => window.location.reload()}
              className="px-5 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-lg text-sm font-medium transition-colors"
            >
              إعادة تحميل الصفحة
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
