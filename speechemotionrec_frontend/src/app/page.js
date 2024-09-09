import Header from "@/components/Header";
import MainForm from "@/components/MainForm";
import ProjectInfo from "@/components/ProjectInfo";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-100 to-red-100">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <MainForm />
        <ProjectInfo />
      </div>
    </div>
  );
}