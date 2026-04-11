interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg";
}

export default function LoadingSpinner({ size = "md" }: LoadingSpinnerProps) {
  const sizeClasses = { sm: "w-5 h-5", md: "w-8 h-8", lg: "w-12 h-12" };
  return (
    <div className="flex items-center justify-center">
      <div className={`relative ${sizeClasses[size]}`}>
        <div className="absolute inset-0 rounded-full border-2 border-quran-gold/20" />
        <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-quran-gold animate-spin" />
        <div className="absolute inset-2 rounded-full bg-quran-gold/10 animate-pulse" />
      </div>
    </div>
  );
}
