export default function CheckMark({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      width="24"
      height="24"
      className={className}
    >
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M6.621 11.379 4.5 13.5l3.182 3.182 2.121 2.121 2.122-2.121 7.424-7.425-2.121-2.121-7.425 7.425z"
        fill="currentColor"
      />
    </svg>
  );
}
