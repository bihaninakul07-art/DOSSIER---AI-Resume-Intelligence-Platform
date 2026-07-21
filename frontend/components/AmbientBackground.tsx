export default function AmbientBackground() {
  return (
    <div
      className="fixed inset-0 pointer-events-none z-0"
      style={{
        background:
          "radial-gradient(ellipse 90% 60% at 50% -10%, rgba(216, 155, 74, 0.06), transparent), " +
          "radial-gradient(ellipse 70% 50% at 100% 100%, rgba(74, 140, 124, 0.05), transparent)",
      }}
    />
  );
}
