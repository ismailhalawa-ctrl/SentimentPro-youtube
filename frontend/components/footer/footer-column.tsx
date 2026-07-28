import Link from 'next/link';
import { Badge } from '@/components/ui/badge';

export interface FooterLink {
  label: string;
  href: string;
  comingSoon?: boolean;
}

export function FooterColumn({ title, links }: { title: string; links: FooterLink[] }) {
  return (
    <div className="flex flex-col gap-3">
      <p className="text-sm font-semibold text-text-primary">{title}</p>
      <ul className="flex flex-col gap-2">
        {links.map((link) => (
          <li key={link.label}>
            {link.comingSoon ? (
              <span className="flex items-center gap-1.5 text-sm text-text-muted">
                {link.label}
                <Badge status="info" className="text-[10px]">
                  Soon
                </Badge>
              </span>
            ) : (
              <Link
                href={link.href}
                className="text-sm text-text-secondary transition-colors duration-150 hover:text-text-primary"
              >
                {link.label}
              </Link>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}