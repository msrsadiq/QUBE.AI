/**
 * Footer Component
 * ----------------
 * Application footer with copyright only.
 */

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-[#17a2b8] text-white py-4 px-6">
      <div className="text-center text-sm">
        © {currentYear} Qube.AI - QE Co-Pilot. All rights reserved.
      </div>
    </footer>
  );
}