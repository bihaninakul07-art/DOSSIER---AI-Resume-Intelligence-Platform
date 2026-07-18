export default function AmbientBackground() {
  return (
    <>
      <div className="blob blob-1 w-[500px] h-[500px] bg-teal top-[-100px] left-[-100px]" />
      <div className="blob blob-2 w-[450px] h-[450px] bg-violet top-[20%] right-[-150px]" />
      <div className="blob blob-1 w-[350px] h-[350px] bg-pink bottom-[-100px] left-[20%]" style={{ animationDelay: "-8s" }} />
    </>
  );
}
