'use client';

import * as React from 'react';
import { createPortal } from 'react-dom';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { AnimatePresence, motion } from 'framer-motion';
import { Menu, X, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

type NavLink = {
  label: string;
  href: string;
  comingSoon?: boolean;
};

const NAV_LINKS: NavLink[] = [
  { label: 'Home', href: '/' },
  { label: 'Features', href: '/#features' },
  { label: 'Pricing', href: '/pricing' },
  { label: 'Documentation', href: '/docs' },
];

function NavLogo() {
  const pathname = usePathname();

  const handleLogoClick = (e: React.MouseEvent) => {
    if (pathname === '/') {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <Link href="/" onClick={handleLogoClick} className="flex items-center gap-2">
      <span className="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-brand">
        <Sparkles className="h-4 w-4 text-text-primary" />
      </span>
      <span className="text-base font-semibold text-text-primary">
        Sentiment<span className="text-brand-400">PRO</span>
      </span>
    </Link>
  );
}

function NavLinkItem({ link, onClick }: { link: NavLink; onClick?: () => void }) {
  const pathname = usePathname();

  if (link.comingSoon) {
    return (
      <span
        className="flex cursor-not-allowed items-center gap-1.5 text-sm font-medium text-text-muted"
        aria-disabled="true"
      >
        {link.label}
        <Badge status="info" className="text-[10px]">
          Soon
        </Badge>
      </span>
    );
  }

  const handleNavigation = (e: React.MouseEvent) => {
    if (pathname !== '/') {
      if (onClick) onClick();
      return;
    }

    if (link.label === 'Home') {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth',
      });
    } else if (link.label === 'Features') {
      e.preventDefault();
      const featuresSection = document.getElementById('features');
      if (featuresSection) {
        featuresSection.scrollIntoView({
          behavior: 'smooth',
          block: 'start',
        });
      }
    }

    if (onClick) onClick();
  };

  return (
    <Link
      href={link.href}
      onClick={handleNavigation}
      className="text-sm font-medium text-text-secondary transition-colors duration-150 hover:text-text-primary"
    >
      {link.label}
    </Link>
  );
}

function NavActions() {
  return (
    <div className="hidden items-center gap-3 md:flex">
      <Link href="/login" passHref>
        <Button variant="ghost" size="sm">
          Login
        </Button>
      </Link>

      <Link href="/register" passHref>
        <Button variant="primary" size="sm">
          Get Started
        </Button>
      </Link>
    </div>
  );
}

const drawerVariants = {
  hidden: { x: '100%', opacity: 0 },
  visible: { x: 0, opacity: 1 },
};

function MobileDrawer({ onClose }: { onClose: () => void }) {
  const closeButtonRef = React.useRef<HTMLButtonElement>(null);

  React.useEffect(() => {
    closeButtonRef.current?.focus();
  }, []);

  return createPortal(
    <>
      <motion.div
        className="fixed inset-0 z-40 bg-background-overlay md:hidden"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.2 }}
        onClick={onClose}
      />
      <motion.div
        role="dialog"
        aria-modal="true"
        aria-label="Mobile navigation"
        className="fixed right-0 top-0 z-50 flex h-full w-72 flex-col gap-6 border-l border-border-default bg-background-elevated p-6 md:hidden"
        variants={drawerVariants}
        initial="hidden"
        animate="visible"
        exit="hidden"
        transition={{ type: 'spring', damping: 28, stiffness: 300 }}
      >
        <div className="flex items-center justify-between">
          <NavLogo />
          <button
            ref={closeButtonRef}
            onClick={onClose}
            aria-label="Close menu"
            className="rounded-md p-1.5 text-text-secondary transition-colors hover:bg-background-surface hover:text-text-primary"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <nav className="flex flex-col gap-4">
          {NAV_LINKS.map((link) => (
            <NavLinkItem key={link.label} link={link} onClick={onClose} />
          ))}
        </nav>

        <div className="mt-auto flex flex-col gap-3">
          <Link href="/login" passHref onClick={onClose} className="w-full">
            <Button variant="secondary" size="md" className="w-full">
              Login
            </Button>
          </Link>

          <Link href="/register" passHref onClick={onClose} className="w-full">
            <Button variant="primary" size="md" className="w-full">
              Get Started
            </Button>
          </Link>
        </div>
      </motion.div>
    </>,
    document.body
  );
}

export function Navbar() {
  const [isOpen, setIsOpen] = React.useState(false);

  React.useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setIsOpen(false);
    };

    document.addEventListener('keydown', handleKeyDown);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = previousOverflow;
    };
  }, [isOpen]);

  return (
    <header className="sticky top-0 z-50 border-b border-border-subtle bg-background-surface/60 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <NavLogo />

        <nav className="hidden items-center gap-8 md:flex">
          {NAV_LINKS.map((link) => (
            <NavLinkItem key={link.label} link={link} />
          ))}
        </nav>

        <NavActions />

        <button
          onClick={() => setIsOpen(true)}
          aria-label="Open menu"
          className="flex items-center justify-center rounded-md p-2 text-text-secondary transition-colors hover:bg-background-elevated hover:text-text-primary md:hidden"
        >
          <Menu className="h-5 w-5" />
        </button>
      </div>

      <AnimatePresence>
        {isOpen && <MobileDrawer onClose={() => setIsOpen(false)} />}
      </AnimatePresence>
    </header>
  );
}