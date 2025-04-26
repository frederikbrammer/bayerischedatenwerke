import type React from 'react';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
    title: 'BayerischeDatenWerke',
    description: 'Litigation Management Tool',
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang='en' className='light' style={{ colorScheme: 'light' }}>
            <body className={inter.className}>
                <main className='h-screen overflow-auto pt-16'>{children}</main>
            </body>
        </html>
    );
}
