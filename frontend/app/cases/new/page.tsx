'use client';

import type React from 'react';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { ArrowLeft, Upload, Loader2 } from 'lucide-react';
import Link from 'next/link';
import { TopNavigation } from '@/components/top-navigation';
import { createCase } from '@/lib/api';

export default function NewCasePage() {
    const router = useRouter();
    const [files, setFiles] = useState<File[]>([]);
    const [isDragging, setIsDragging] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        if (e.dataTransfer.files) {
            const newFiles = Array.from(e.dataTransfer.files);
            setFiles((prev) => [...prev, ...newFiles]);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
            const newFiles = Array.from(e.target.files);
            setFiles((prev) => [...prev, ...newFiles]);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            // Create a FormData object to send files
            const formData = new FormData();

            // Append each file to the form data - FastAPI expects "files" as the field name
            files.forEach((file) => {
                formData.append('files', file);
            });

            // Send the form data to the backend
            const response = await createCase(formData);

            // Redirect to the new case page
            router.push(`/cases/${response.id}`);
        } catch (error) {
            console.error('Error creating case:', error);
            alert('Failed to create case. Please try again.');
            setIsSubmitting(false);
        }
    };

    return (
        <>
            <TopNavigation />
            <div className='container mx-auto p-6'>
                <div className='mb-6'>
                    <Button asChild variant='outline' size='sm'>
                        <Link href='/cases'>
                            <ArrowLeft className='mr-2 h-4 w-4' /> Back to Cases
                        </Link>
                    </Button>
                </div>

                <h1 className='text-3xl font-bold mb-6'>Create New Case</h1>

                <form onSubmit={handleSubmit}>
                    <div className='mb-6'>
                        <Card>
                            <CardContent className='p-6'>
                                <div
                                    className={`border-2 border-dashed rounded-lg p-6 text-center ${
                                        isDragging
                                            ? 'border-primary bg-primary/5'
                                            : 'border-muted-foreground/20'
                                    }`}
                                    onDragOver={handleDragOver}
                                    onDragLeave={handleDragLeave}
                                    onDrop={handleDrop}
                                >
                                    <Upload className='h-10 w-10 mx-auto mb-4 text-muted-foreground' />
                                    <h3 className='text-lg font-medium mb-2'>
                                        Drag & Drop Documents
                                    </h3>
                                    <p className='text-sm text-muted-foreground mb-4'>
                                        Drop all documents & evidence related to
                                        this case
                                    </p>
                                    <p className='text-sm text-muted-foreground mb-4'>
                                        Case title, jurisdiction, and case type
                                        will be extracted automatically from the
                                        documents
                                    </p>
                                    <div className='relative'>
                                        <Input
                                            type='file'
                                            multiple
                                            className='absolute inset-0 opacity-0 cursor-pointer'
                                            onChange={handleFileChange}
                                            accept='.pdf,.doc,.docx,.txt'
                                        />
                                        <Button variant='outline' type='button'>
                                            Browse Files
                                        </Button>
                                    </div>
                                </div>

                                {files.length > 0 && (
                                    <div className='mt-4'>
                                        <h4 className='font-medium mb-2'>
                                            Uploaded Files ({files.length})
                                        </h4>
                                        <ul className='space-y-2 max-h-40 overflow-y-auto'>
                                            {files.map((file, index) => (
                                                <li
                                                    key={index}
                                                    className='text-sm text-muted-foreground'
                                                >
                                                    {file.name}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </div>

                    <div className='flex justify-end'>
                        <Button
                            type='submit'
                            disabled={isSubmitting || files.length === 0}
                        >
                            {isSubmitting ? (
                                <>
                                    <Loader2 className='mr-2 h-4 w-4 animate-spin' />
                                    Creating...
                                </>
                            ) : (
                                'Create Case'
                            )}
                        </Button>
                    </div>
                </form>
            </div>
        </>
    );
}
