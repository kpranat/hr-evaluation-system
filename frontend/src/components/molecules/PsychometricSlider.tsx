import { useState } from 'react';
import * as SliderPrimitive from '@radix-ui/react-slider';
import { cn } from '@/lib/utils';

interface PsychometricSliderProps {
  value: number | undefined;
  onChange: (value: number) => void;
  labels?: string[];
}

export function PsychometricSlider({ value, onChange, labels }: PsychometricSliderProps) {
  const [isDragging, setIsDragging] = useState(false);
  
  const defaultLabels = [
    'Very Inaccurate',
    'Moderately Inaccurate',
    'Neither Accurate Nor Inaccurate',
    'Moderately Accurate',
    'Very Accurate'
  ];
  
  const displayLabels = labels || defaultLabels;
  const points = [1, 2, 3, 4, 5];
  
  // Get position percentage for each point
  const getPosition = (point: number) => ((point - 1) / 4) * 100;
  
  // Calculate size for markers (larger at ends, smaller in middle)
  const getMarkerSize = (point: number) => {
    if (point === 1 || point === 5) return 'h-4 w-4'; // Largest at ends
    if (point === 2 || point === 4) return 'h-3 w-3'; // Medium
    return 'h-2 w-2'; // Smallest in middle
  };

  return (
    <div className="w-full space-y-8">
      {/* Slider Container */}
      <div className="relative pt-8 pb-12">
        {/* Uniform Track */}
        <div className="relative h-12 flex items-center">
          {/* Background track - uniform height */}
          <div className="absolute inset-0 flex items-center">
            <div className="relative w-full h-2 rounded-full bg-muted" />
          </div>
          
          {/* Active track overlay - uniform height */}
          {value && value > 1 && (
            <div className="absolute inset-0 flex items-center pointer-events-none">
              <div 
                className="h-2 rounded-l-full bg-primary" 
                style={{ width: `${getPosition(value)}%` }} 
              />
            </div>
          )}
          
          {/* Position markers - concentric circles */}
          <div className="absolute inset-0 flex items-center justify-between pointer-events-none">
            {points.map((point) => {
              const isSelected = value === point;
              
              return (
                <div
                  key={point}
                  className="flex items-center justify-center"
                  style={{ width: '40px', height: '40px' }}
                >
                  {/* Outer ring */}
                  <div
                    className={cn(
                      'absolute rounded-full transition-all border-2',
                      getMarkerSize(point),
                      isSelected
                        ? 'bg-primary border-primary'
                        : 'bg-background border-muted-foreground/40'
                    )}
                  />
                  {/* Inner dot for non-selected markers */}
                  {!isSelected && (
                    <div
                      className={cn(
                        'absolute rounded-full bg-muted-foreground/40',
                        point === 1 || point === 5 ? 'h-2 w-2' : point === 2 || point === 4 ? 'h-1.5 w-1.5' : 'h-1 w-1'
                      )}
                    />
                  )}
                </div>
              );
            })}
          </div>
          
          {/* Radix Slider with draggable thumb */}
          <SliderPrimitive.Root
            min={1}
            max={5}
            step={1}
            value={[value || 1]}
            onValueChange={(vals) => onChange(vals[0])}
            onPointerDown={() => setIsDragging(true)}
            onPointerUp={() => setIsDragging(false)}
            className="absolute inset-0 flex items-center w-full cursor-pointer"
          >
            <SliderPrimitive.Track className="relative h-12 w-full">
              <SliderPrimitive.Range className="absolute h-full opacity-0" />
            </SliderPrimitive.Track>
            <SliderPrimitive.Thumb 
              className={cn(
                "block h-10 w-10 rounded-full border-4 border-primary bg-background shadow-lg transition-all z-10",
                "focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-primary/20",
                "hover:scale-110 active:scale-105",
                isDragging && "scale-110 ring-4 ring-primary/30"
              )}
            />
          </SliderPrimitive.Root>
        </div>
        
        {/* Labels */}
        <div className="flex justify-between mt-8 px-1">
          {displayLabels.map((label, idx) => {
            const point = idx + 1;
            const isSelected = value === point;
            
            return (
              <div
                key={idx}
                className={cn(
                  'text-center transition-all',
                  idx === 0 || idx === displayLabels.length - 1 ? 'w-32' : 'w-28'
                )}
              >
                <span
                  className={cn(
                    'text-sm transition-all block',
                    isSelected
                      ? 'font-bold text-primary scale-105'
                      : 'text-muted-foreground'
                  )}
                >
                  {label}
                </span>
              </div>
            );
          })}
        </div>
      </div>
      
      {/* Current Selection Display */}
      {value && (
        <div className="text-center p-4 rounded-lg bg-muted/50 border border-border">
          <p className="text-sm text-muted-foreground mb-1">Your response:</p>
          <p className="text-lg font-semibold text-foreground">
            {displayLabels[value - 1]}
          </p>
        </div>
      )}
    </div>
  );
}
