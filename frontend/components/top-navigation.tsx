'use client';

import Link from 'next/link';
import Image from 'next/image';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';

export function TopNavigation() {
    const pathname = usePathname();

    const isActive = (path: string) => {
        return pathname === path || pathname.startsWith(`${path}/`);
    };

    return (
        <div className='border-b fixed top-0 left-0 right-0 z-10 bg-white'>
            <div className='container mx-auto px-6'>
                <div className='flex items-center justify-between h-16'>
                    <div className='flex items-center space-x-2'>
                        <Image
                            src='/bmw.svg'
                            alt='BMW Logo'
                            width={32}
                            height={32}
                        />
                        <h1 className='text-xl font-bold pl-2'>
                            Litigation Manager
                        </h1>
                    </div>

                    <nav className='flex space-x-4 absolute left-1/2 transform -translate-x-1/2'>
                        <Link
                            href='/cases'
                            className={cn(
                                'px-4 py-2 rounded-full text-sm font-medium transition-colors',
                                isActive('/cases')
                                    ? 'text-blue-600 bg-blue-100/80'
                                    : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
                            )}
                        >
                            Cases
                        </Link>
                        <Link
                            href='/trends'
                            className={cn(
                                'px-4 py-2 rounded-full text-sm font-medium transition-colors',
                                isActive('/trends')
                                    ? 'text-blue-600 bg-blue-100/80'
                                    : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
                            )}
                        >
                            Trends
                        </Link>
                    </nav>
                </div>
            </div>
        </div>
    );
}
