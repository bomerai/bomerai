export default function Check({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      width="24"
      height="24"
      className={className}
    >
      <g clipPath="url(#check_svg__a)">
        <path
          d="m10 15.172 9.192-9.193 1.415 1.414L10 18l-6.364-6.364 1.414-1.414z"
          fill="currentColor"
        />
      </g>
      <defs>
        <clipPath id="check_svg__a">
          <rect width={24} height={24} fill="white" />
        </clipPath>
      </defs>
    </svg>
  );
}
