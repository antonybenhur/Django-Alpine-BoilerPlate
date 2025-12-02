CRIUS Design System (Geist Clone)

Tech Stack: Django Templates, Tailwind CSS v3+, Alpine.js v3+
Design Philosophy: Minimalist, Swiss-style, Content-first (Vercel/Geist aesthetic).

1. Configuration & Tokens

A. Tailwind Configuration (tailwind.config.js)

This configuration maps Vercel's proprietary tokens to standard Tailwind utility classes.

module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Geist Sans"', 'sans-serif'],
        mono: ['"Geist Mono"', 'monospace'],
      },
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem', letterSpacing: '0' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem', letterSpacing: '0' }],
        'base': ['1rem', { lineHeight: '1.5rem', letterSpacing: '-0.01em' }],
        'lg': ['1.5rem', { lineHeight: '1.75rem', letterSpacing: '-0.02em', fontWeight: '600' }],
        'xl': ['2rem', { lineHeight: '2.25rem', letterSpacing: '-0.02em', fontWeight: '700' }],
        '2xl': ['3rem', { lineHeight: '1', letterSpacing: '-0.03em', fontWeight: '800' }],
        '3xl': ['4rem', { lineHeight: '1', letterSpacing: '-0.04em', fontWeight: '800' }],
      },
      letterSpacing: {
        tighter: '-0.05em',
        tight: '-0.02em',
        normal: '-0.01em',
        wide: '0.02em',
      },
      colors: {
        gray: {
          50:  '#f9fafb',
          100: '#fafafa', // App Background
          200: '#eaeaea', // Borders
          300: '#999999', // Subtle Text
          400: '#888888', // Secondary Text
          500: '#666666', // Icons / Meta
          600: '#444444',
          700: '#333333',
          800: '#111111', // Dark Accents
          900: '#000000', // Headings
        },
        blue: {
          geist: '#0070f3', // Primary Brand
          dark: '#0761d1',
          light: '#3291ff',
        },
        red: {
          geist: '#e00000', // Error
          light: '#ff1a1a',
          dark: '#c50000',
        },
        amber: {
          geist: '#f5a623', // Warning
          400: '#f5a623',
        },
        violet: {
          geist: '#7928ca', // Beta/Feature
        },
        cyan: {
          geist: '#50e3c2', // Success
        },
      },
      boxShadow: {
        'geist': '0 0 0 1px rgba(0,0,0,0.08), 0 4px 6px rgba(0,0,0,0.04)',
        'geist-hover': '0 0 0 1px rgba(0,0,0,0.08), 0 6px 14px rgba(0,0,0,0.08)',
        'geist-active': '0 0 0 1px #000',
      },
      borderRadius: {
        'geist': '6px',
      }
    }
  }
}


B. Global CSS (styles.css)

Handles fonts, custom animations, and "Material" utility classes.

@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
    /* Glassmorphism Materials */
    .material-base {
        @apply bg-white/80 backdrop-blur-[20px] backdrop-saturate-150 border border-gray-200;
        @apply dark:bg-black/80 dark:border-gray-800;
    }
    .material-menu {
        @apply bg-white/90 backdrop-blur-[24px] backdrop-saturate-150 shadow-geist-hover border border-gray-200 rounded-geist;
    }
    .material-modal {
        @apply bg-white/95 backdrop-blur-[32px] backdrop-saturate-150 shadow-2xl border border-gray-200 rounded-xl;
    }
    .material-tooltip {
        @apply bg-black text-white text-xs px-2 py-1 rounded shadow-lg;
    }
}

/* Animations */
@keyframes geist-blink {
    0% { opacity: 0.2; }
    20% { opacity: 1; }
    100% { opacity: 0.2; }
}
.loading-dot { animation: geist-blink 1.4s infinite both; }
.loading-dot:nth-child(2) { animation-delay: 0.2s; }
.loading-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes shimmer {
    100% { transform: translateX(100%); }
}
.skeleton-shimmer {
    position: relative;
    overflow: hidden;
    background-color: #fafafa;
}
.skeleton-shimmer::after {
    position: absolute;
    top: 0; right: 0; bottom: 0; left: 0;
    transform: translateX(-100%);
    background-image: linear-gradient(90deg, rgba(255,255,255,0) 0, rgba(255,255,255,0.5) 20%, rgba(255,255,255,0.8) 60%, rgba(255,255,255,0));
    animation: shimmer 2s infinite;
    content: '';
}


2. Atoms (Primitive Components)

Avatar

File: templates/components/avatar.html
Description: Fallback to gradient, status indicator.

{% with size=size|default:'32' alt=alt|default:'Avatar' %}
<div class="relative inline-block rounded-full overflow-hidden bg-gray-100 ring-1 ring-gray-200 grayscale-[0] hover:grayscale-0 transition-all duration-200"
    style="width: {{ size }}px; height: {{ size }}px;"
    x-data="{ src: '{{ src|default:'' }}', fallback: '[https://avatar.vercel.sh/](https://avatar.vercel.sh/){{ alt|urlencode }}?size={{ size }}' }">
    <img :src="src || fallback" alt="{{ alt }}" @error="src = fallback" class="w-full h-full object-cover" width="{{ size }}" height="{{ size }}">
    {% if status %}
    <span class="absolute bottom-0 right-0 block rounded-full ring-2 ring-white {% if status == 'online' %}bg-green-500{% elif status == 'busy' %}bg-red-geist{% elif status == 'away' %}bg-amber-400{% else %}bg-gray-400{% endif %}"
        style="width: {{ size|add:'-24'|default:'8' }}px; height: {{ size|add:'-24'|default:'8' }}px; min-width: 8px; min-height: 8px;"></span>
    {% endif %}
</div>
{% endwith %}


Usage:

{% include "components/avatar.html" with src=user.img size=32 status="online" %}


Badge / Pill

File: templates/components/badge.html

{% with variant=variant|default:'gray' size=size|default:'md' shape=shape|default:'square' %}
<span class="inline-flex items-center justify-center font-medium border border-transparent whitespace-nowrap
    {% if shape == 'pill' %}rounded-full{% else %}rounded-geist{% endif %}
    {% if size == 'sm' %}px-2 py-0.5 text-xs h-5{% elif size == 'lg' %}px-3 py-1 text-sm h-7{% else %}px-2.5 py-0.5 text-xs h-6{% endif %}
    {% if variant == 'gray' %}bg-gray-100 text-gray-600
    {% elif variant == 'blue' %}bg-blue-50 text-blue-geist
    {% elif variant == 'red' %}bg-red-50 text-red-600
    {% elif variant == 'amber' %}bg-amber-50 text-amber-600
    {% elif variant == 'violet' %}bg-violet-50 text-violet-600
    {% elif variant == 'outline' %}bg-transparent border-gray-200 text-gray-600{% endif %}
    {{ class }}">
    {% if dot %}
    <span class="mr-1.5 -ml-0.5 w-1.5 h-1.5 rounded-full {% if variant == 'gray' %}bg-gray-500{% elif variant == 'blue' %}bg-blue-geist{% elif variant == 'red' %}bg-red-geist{% elif variant == 'amber' %}bg-amber-400{% endif %}"></span>
    {% endif %}
    {{ slot }}
</span>
{% endwith %}


Usage:

{% include "components/badge.html" with variant="blue" dot=True slot="Deploying" %}


Button

File: templates/components/button.html

{% with type=type|default:'button' variant=variant|default:'primary' size=size|default:'md' width=width|default:'auto' %}
<button type="{{ type }}" {% if disabled or loading %}disabled{% endif %}
    class="group relative inline-flex items-center justify-center font-medium transition-all duration-200 ease-in-out border select-none rounded-geist
        {% if size == 'sm' %}h-8 px-3 text-sm{% elif size == 'lg' %}h-12 px-6 text-base{% else %}h-10 px-4 text-sm{% endif %}
        {% if width == 'full' %}w-full flex{% endif %}
        {% if variant == 'primary' %}bg-gray-900 border-transparent text-white hover:bg-gray-800 disabled:bg-gray-100 disabled:text-gray-400 disabled:border-gray-200
        {% elif variant == 'secondary' %}bg-white border-gray-200 text-gray-900 hover:border-gray-500 hover:bg-gray-50 disabled:bg-gray-50 disabled:text-gray-400
        {% elif variant == 'error' %}bg-red-50 border-red-200 text-red-600 hover:bg-red-100 hover:border-red-300
        {% elif variant == 'ghost' %}bg-transparent border-transparent text-gray-600 hover:bg-gray-100 hover:text-gray-900{% endif %}
        {{ class }}"
    {% if action %}@click="{{ action }}"{% endif %}>
    {% if loading %}
        <div class="absolute inset-0 flex items-center justify-center">{% include "components/loading_dots.html" %}</div>
        <div class="invisible flex items-center gap-2">{{ slot }}</div>
    {% else %}
        <div class="flex items-center gap-2">
            {% if prefix %}<span class="text-current opacity-60">{{ prefix }}</span>{% endif %}
            <span>{{ slot }}</span>
            {% if suffix %}<span class="text-current opacity-60">{{ suffix }}</span>{% endif %}
        </div>
    {% endif %}
</button>
{% endwith %}


Usage:

{% include "components/button.html" with variant="primary" loading=is_loading slot="Deploy" %}


Loading Dots

File: templates/components/loading_dots.html

<span class="inline-flex items-center gap-1 h-full py-1">
    <span class="w-1 h-1 bg-current rounded-full loading-dot"></span>
    <span class="w-1 h-1 bg-current rounded-full loading-dot"></span>
    <span class="w-1 h-1 bg-current rounded-full loading-dot"></span>
</span>


Status Dot

File: templates/components/status_dot.html

{% with state=state|default:'ready' label=label %}
<div class="flex items-center gap-2 {{ class }}">
    <span class="block w-2.5 h-2.5 rounded-full
        {% if state == 'ready' %}bg-blue-geist
        {% elif state == 'error' %}bg-red-geist
        {% elif state == 'queued' %}bg-gray-300
        {% elif state == 'canceled' %}bg-gray-300
        {% elif state == 'building' %}bg-amber-400 animate-pulse{% endif %}">
    </span>
    {% if label %}<span class="text-sm text-gray-600 capitalize">{{ label }}</span>{% endif %}
</div>
{% endwith %}


3. Form Elements

Input

File: templates/components/input.html

{% with type=type|default:'text' name=name|default:'' id=id|default:name label=label value=value|default:'' placeholder=placeholder|default:'' error=error disabled=disabled %}
<div class="flex flex-col gap-1.5 w-full {{ wrapper_class }}">
    {% if label %}<label for="{{ id }}" class="text-xs font-medium text-gray-500 uppercase tracking-wide">{{ label }}</label>{% endif %}
    <div class="relative flex items-center group">
        {% if prefix %}<span class="absolute left-3 text-gray-400 text-sm pointer-events-none select-none">{{ prefix }}</span>{% endif %}
        <input type="{{ type }}" name="{{ name }}" id="{{ id }}" value="{{ value }}" placeholder="{{ placeholder }}" {% if disabled %}disabled{% endif %}
            class="flex h-10 w-full rounded-geist border bg-white px-3 py-2 text-sm text-gray-900 transition-colors focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 disabled:cursor-not-allowed disabled:bg-gray-50 disabled:text-gray-400 placeholder:text-gray-400
            {% if prefix %}pl-8{% endif %} {% if suffix %}pr-8{% endif %}
            {% if error %}border-red-geist focus:border-red-geist focus:ring-red-geist text-red-900{% else %}border-gray-200 hover:border-gray-400{% endif %} {{ class }}">
        {% if suffix %}<span class="absolute right-3 text-gray-400 text-sm pointer-events-none select-none">{{ suffix }}</span>{% endif %}
    </div>
    {% if error %}<span class="text-xs text-red-geist mt-0.5">{{ error }}</span>{% endif %}
</div>
{% endwith %}


Usage:

{% include "components/input.html" with label="Domain" prefix="https://" error=form.errors.domain %}


Textarea

File: templates/components/textarea.html

{% with name=name|default:'' id=id|default:name label=label value=value|default:'' rows=rows|default:'4' placeholder=placeholder|default:'' error=error %}
<div class="flex flex-col gap-1.5 w-full {{ wrapper_class }}">
    {% if label %}<label for="{{ id }}" class="text-xs font-medium text-gray-500 uppercase tracking-wide">{{ label }}</label>{% endif %}
    <textarea name="{{ name }}" id="{{ id }}" rows="{{ rows }}" placeholder="{{ placeholder }}"
        class="flex w-full rounded-geist border bg-white px-3 py-2 text-sm text-gray-900 transition-colors focus:outline-none focus:ring-1 focus:ring-gray-900 focus:border-gray-900 placeholder:text-gray-400 {% if error %}border-red-geist focus:border-red-geist focus:ring-red-geist{% else %}border-gray-200 hover:border-gray-400{% endif %} {{ class }}">{{ value }}</textarea>
    {% if error %}<span class="text-xs text-red-geist">{{ error }}</span>{% endif %}
</div>
{% endwith %}


Checkbox

File: templates/components/checkbox.html

{% with name=name|default:'' id=id|default:name label=label checked=checked disabled=disabled %}
<div class="flex items-start gap-3">
    <div class="relative flex items-center">
        <input type="checkbox" id="{{ id }}" name="{{ name }}" {% if checked %}checked{% endif %} {% if disabled %}disabled{% endif %}
            class="peer h-5 w-5 appearance-none rounded border border-gray-300 bg-white transition-all checked:bg-gray-900 checked:border-gray-900 focus:outline-none focus:ring-2 focus:ring-gray-200 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50">
        <svg class="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-white opacity-0 peer-checked:opacity-100 transition-opacity w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
    </div>
    {% if label %}<label for="{{ id }}" class="text-sm text-gray-900 pt-0.5 select-none cursor-pointer peer-disabled:cursor-not-allowed peer-disabled:text-gray-400">{{ label }}</label>{% endif %}
</div>
{% endwith %}


Toggle / Switch

File: templates/components/toggle.html

{% with name=name|default:'' id=id|default:name label=label checked=checked %}
<div x-data="{ on: {{ checked|yesno:'true,false' }} }" class="flex items-center justify-between gap-4">
    {% if label %}<label @click="$refs.toggleBtn.click()" class="text-sm font-medium text-gray-900 cursor-pointer">{{ label }}</label>{% endif %}
    <input type="hidden" name="{{ name }}" :value="on ? 'True' : 'False'">
    <button x-ref="toggleBtn" type="button" role="switch" :aria-checked="on" @click="on = !on" :class="on ? 'bg-gray-900' : 'bg-gray-200'" class="relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-gray-200 focus:ring-offset-2">
        <span :class="on ? 'translate-x-5' : 'translate-x-0'" class="pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"></span>
    </button>
</div>
{% endwith %}


Select (Native)

File: templates/components/select_native.html

{% with name=name|default:'' id=id|default:name label=label options=options %}
<div class="flex flex-col gap-1.5 w-full">
    {% if label %}<label for="{{ id }}" class="text-xs font-medium text-gray-500 uppercase tracking-wide">{{ label }}</label>{% endif %}
    <div class="relative">
        <select name="{{ name }}" id="{{ id }}" class="appearance-none flex h-10 w-full rounded-geist border border-gray-200 bg-white px-3 py-2 text-sm text-gray-900 focus:border-gray-900 focus:outline-none focus:ring-1 focus:ring-gray-900 disabled:cursor-not-allowed disabled:bg-gray-50 pr-8">
            {{ slot }} 
        </select>
        <div class="pointer-events-none absolute top-0 right-0 flex h-full w-8 items-center justify-center text-gray-500">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4"><path d="m6 9 6 6 6-6"/></svg>
        </div>
    </div>
</div>
{% endwith %}


4. Molecules (Containers & Feedback)

Card

File: templates/components/card.html

<div class="rounded-geist border border-gray-200 bg-white overflow-hidden flex flex-col {{ class }}">
    {% if title %}
    <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900 leading-6">{{ title }}</h3>
        {% if action %}<div>{{ action }}</div>{% endif %}
    </div>
    {% endif %}
    <div class="p-6 text-sm text-gray-500 {{ content_class }}">{{ slot }}</div>
    {% if footer %}
    <div class="bg-gray-50 px-6 py-3 border-t border-gray-200 text-xs text-gray-500 flex items-center justify-between">{{ footer }}</div>
    {% endif %}
</div>


Usage:

{% include "components/card.html" with title="Settings" footer="Saved just now" %}


Snippet

File: templates/components/snippet.html

{% with text=text|default:'npm install' width=width|default:'auto' type=type|default:'default' %}
<div x-data="{ text: '{{ text|escapejs }}', copied: false, copy() { navigator.clipboard.writeText(this.text); this.copied = true; setTimeout(() => this.copied = false, 2000); } }"
    class="group relative border rounded-geist px-4 py-3 font-mono text-sm flex items-center justify-between {% if type == 'dark' %}bg-black text-white border-black{% elif type == 'lite' %}bg-gray-50 border-gray-200 text-gray-800{% else %}bg-white border-gray-200 text-gray-800{% endif %} {{ class }}" style="width: {{ width }}">
    <span class="truncate pr-8 select-all"><span class="text-gray-400 select-none">$ </span>{{ text }}</span>
    <button @click="copy()" class="absolute right-2 p-1.5 rounded-md transition-all opacity-0 group-hover:opacity-100 focus:opacity-100" :class="copied ? 'text-green-500' : 'text-gray-400 hover:bg-gray-200 hover:text-gray-900'" title="Copy to clipboard">
        <svg x-show="!copied" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
        <svg x-show="copied" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
    </button>
</div>
{% endwith %}


Modal / Dialog

File: templates/components/modal.html

{% with id=id|default:'modal' title=title trigger_text=trigger_text %}
<div x-data="{ open: false }" @keydown.escape.window="open = false" class="relative inline-block">
    {% if trigger_text %}
    <button @click="open = true" class="btn btn-secondary text-sm px-4 py-2 border rounded-geist hover:border-gray-500 transition-colors">{{ trigger_text }}</button>
    {% endif %}
    <div x-show="open" x-transition.opacity class="fixed inset-0 bg-black/50 backdrop-blur-sm z-40" aria-hidden="true"></div>
    <div x-show="open" style="display: none;" x-transition:enter="transition ease-out duration-300" x-transition:enter-start="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" x-transition:enter-end="opacity-100 translate-y-0 sm:scale-100" x-transition:leave="transition ease-in duration-200" x-transition:leave-start="opacity-100 translate-y-0 sm:scale-100" x-transition:leave-end="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95" @click.outside="open = false" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-xl shadow-2xl w-full max-w-lg overflow-hidden border border-gray-200">
            {% if title %}
            <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center">
                <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
                <button @click="open = false" class="text-gray-400 hover:text-gray-600"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg></button>
            </div>
            {% endif %}
            <div class="p-6">{{ slot }}</div>
            <div class="bg-gray-50 px-6 py-4 border-t border-gray-100 flex justify-end gap-3">
                <button @click="open = false" class="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 font-medium">Cancel</button>
                <button class="px-4 py-2 text-sm bg-gray-900 text-white rounded-geist hover:bg-black font-medium">Confirm</button>
            </div>
        </div>
    </div>
</div>
{% endwith %}


Empty State

File: templates/components/empty_state.html

{% with title=title description=description action=action %}
<div class="flex flex-col items-center justify-center py-16 px-4 text-center bg-gray-50 rounded-geist border border-dashed border-gray-300">
    <div class="bg-white p-3 rounded-full border border-gray-200 mb-4 shadow-sm">
        <svg class="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>
    </div>
    <h3 class="text-lg font-medium text-gray-900 mb-1">{{ title }}</h3>
    <p class="text-sm text-gray-500 max-w-sm mb-6">{{ description }}</p>
    {% if action %}{{ action }}{% endif %}
</div>
{% endwith %}


File Upload

File: templates/components/file_upload.html

<div x-data="{ dragging: false }" class="w-full">
    <label class="flex flex-col items-center justify-center w-full h-48 border border-dashed rounded-geist cursor-pointer transition-colors"
        :class="dragging ? 'border-blue-geist bg-blue-50' : 'border-gray-300 hover:bg-gray-50 hover:border-gray-400'"
        @dragover.prevent="dragging = true" @dragleave.prevent="dragging = false" @drop.prevent="dragging = false">
        <div class="flex flex-col items-center justify-center pt-5 pb-6">
            <svg class="w-8 h-8 mb-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>
            <p class="mb-2 text-sm text-gray-500"><span class="font-semibold text-gray-900">Click to upload</span> or drag and drop</p>
            <p class="text-xs text-gray-400">SVG, PNG, JPG or GIF (MAX. 800x400px)</p>
        </div>
        <input type="file" class="hidden" />
    </label>
</div>


5. Data Visualization

Data Table

File: templates/components/table.html

<div class="w-full overflow-x-auto rounded-geist border border-gray-200">
    <table class="w-full text-left text-sm text-gray-600 bg-white">
        <thead class="bg-gray-50 text-xs uppercase font-medium text-gray-500">
            <tr>
                {% for header in headers %}
                <th scope="col" class="px-6 py-3 tracking-wider border-b border-gray-200">{{ header }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">{{ slot }}</tbody>
    </table>
</div>


Gauge / Donut

File: templates/components/gauge.html

{% with value=value|default:0 size=size|default:32 max=100 %}
<div class="relative flex items-center justify-center" style="width: {{ size }}px; height: {{ size }}px;">
    <svg class="transform -rotate-90 w-full h-full" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="40" fill="transparent" stroke="#eaeaea" stroke-width="12" />
        <circle cx="50" cy="50" r="40" fill="transparent" stroke="currentColor" stroke-width="12" stroke-dasharray="251.2" stroke-dashoffset="calc(251.2 - (251.2 * {{ value }} / {{ max }}))" stroke-linecap="round" class="transition-all duration-1000 ease-out {% if value > 90 %}text-red-geist{% elif value > 75 %}text-amber-400{% else %}text-blue-geist{% endif %}" />
    </svg>
    {% if show_text %}<span class="absolute text-xs font-medium text-gray-900">{{ value }}%</span>{% endif %}
</div>
{% endwith %}


Progress Bar

File: templates/components/progress.html

{% with value=value|default:0 max=100 color=color|default:'blue' %}
<div class="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
    <div class="h-full rounded-full transition-all duration-500 ease-out {% if color == 'blue' %}bg-blue-geist{% elif color == 'red' %}bg-red-geist{% elif color == 'gray' %}bg-gray-900{% endif %}" style="width: {{ value }}%"></div>
</div>
{% endwith %}


Skeleton

File: templates/components/skeleton.html

{% with width=width|default:'w-full' height=height|default:'h-4' rounded=rounded|default:'rounded-geist' %}
<div class="skeleton-shimmer {{ width }} {{ height }} {{ rounded }} {{ class }}"></div>
{% endwith %}


Entity Item

File: templates/components/entity.html

<div class="flex items-center justify-between p-4 border border-gray-200 rounded-geist bg-white hover:border-gray-400 transition-colors group cursor-pointer">
    <div class="flex items-center gap-4">
        <div class="w-10 h-10 rounded-full bg-gray-100 border border-gray-200 flex items-center justify-center text-gray-500 font-bold text-xs uppercase">{{ initials|default:'PR' }}</div>
        <div>
            <h4 class="font-medium text-gray-900 leading-tight">{{ title }}</h4>
            <p class="text-sm text-gray-500 pt-0.5">{{ description }}</p>
        </div>
    </div>
    <div class="flex items-center gap-4">
        <div class="text-xs text-gray-500 text-right hidden sm:block"><p>Updated {{ time_ago }}</p></div>
        <svg class="w-5 h-5 text-gray-300 group-hover:text-gray-900 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
    </div>
</div>


6. Layouts & Global Components

Global Navbar

File: templates/layout/navbar.html

<header class="sticky top-0 z-50 w-full material-base border-b-0">
    <div class="border-b border-gray-200">
        <div class="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
            <div class="flex items-center gap-4">
                <a href="/" class="text-black hover:opacity-70 transition-opacity">
                    <svg class="h-6 w-6" viewBox="0 0 116 100" fill="currentColor"><path fill-rule="evenodd" clip-rule="evenodd" d="M57.5 0L115 100H0L57.5 0Z" /></svg>
                </a>
                <span class="text-gray-300 text-2xl font-light transform -rotate-[15deg] select-none">/</span>
                <div class="relative" x-data="{ open: false }">
                    <button @click="open = !open" class="flex items-center gap-2 text-sm font-medium text-gray-900 hover:bg-gray-100 px-2 py-1 rounded-geist transition-colors">
                        <span class="w-5 h-5 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500"></span>
                        <span>{{ request.user.username|default:'CRIUS' }}</span>
                        <svg class="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l4-4 4 4m0 6l-4 4-4-4" /></svg>
                    </button>
                    <div x-show="open" @click.outside="open = false" style="display: none;" class="absolute top-full left-0 mt-2 w-64 material-menu p-1">
                        <div class="px-2 py-1.5 text-xs text-gray-500 font-medium">Personal Account</div>
                        <a href="#" class="flex items-center gap-2 px-2 py-2 text-sm text-gray-900 bg-gray-50 rounded-md"><span class="w-5 h-5 rounded-full bg-black"></span>{{ request.user.username }}</a>
                    </div>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <button class="hidden sm:flex text-xs font-medium text-gray-500 border border-gray-200 rounded-geist px-2 py-1 hover:border-gray-400 hover:text-gray-900 transition-colors">Feedback</button>
                <div class="relative ml-2" x-data="{ open: false }">
                    <button @click="open = !open" class="block rounded-full hover:ring-2 hover:ring-gray-200 transition-all">{% include "components/avatar.html" with size=28 %}</button>
                    <div x-show="open" @click.outside="open = false" style="display: none;" class="absolute top-full right-0 mt-2 w-56 material-menu p-1">
                        <a href="#" class="block px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-md">Log Out</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% if not hide_tabs %}
    <div class="border-b border-gray-200">
        <div class="max-w-5xl mx-auto px-6">
            <nav class="flex gap-6 overflow-x-auto no-scrollbar" aria-label="Tabs">
                {% with active_tab=active_tab|default:'overview' %}
                <a href="/dashboard" class="relative py-3 text-sm font-medium transition-colors whitespace-nowrap {% if active_tab == 'overview' %}text-gray-900{% else %}text-gray-500 hover:text-gray-900{% endif %}">Overview {% if active_tab == 'overview' %}<span class="absolute bottom-0 left-0 w-full h-[2px] bg-black"></span>{% endif %}</a>
                <a href="/settings" class="relative py-3 text-sm font-medium transition-colors whitespace-nowrap {% if active_tab == 'settings' %}text-gray-900{% else %}text-gray-500 hover:text-gray-900{% endif %}">Settings {% if active_tab == 'settings' %}<span class="absolute bottom-0 left-0 w-full h-[2px] bg-black"></span>{% endif %}</a>
                {% endwith %}
            </nav>
        </div>
    </div>
    {% endif %}
</header>


Toast Notification

File: templates/layout/toasts.html
Note: Add to bottom of base.html.

<div x-data="{ notifications: [], add(e) { this.notifications.push({ id: Date.now(), message: e.detail.message, type: e.detail.type || 'default', }); }, remove(id) { this.notifications = this.notifications.filter(n => n.id !== id); } }"
    @notify.window="add($event)" class="fixed bottom-6 right-6 z-50 flex flex-col gap-2 w-full max-w-sm pointer-events-none">
    <template x-for="note in notifications" :key="note.id">
        <div class="pointer-events-auto shadow-geist-hover rounded-geist p-4 border flex items-center justify-between transition-all duration-300 transform translate-y-0 opacity-100"
            :class="{ 'bg-white border-gray-200 text-gray-900': note.type === 'default', 'bg-red-geist text-white border-red-geist': note.type === 'error', 'bg-gray-900 text-white border-gray-900': note.type === 'success' }"
            x-transition:enter="translate-y-4 opacity-0" x-transition:leave="opacity-0 scale-95" x-init="setTimeout(() => remove(note.id), 4000)">
            <span class="text-sm font-medium" x-text="note.message"></span>
        </div>
    </template>
</div>


Command Menu (Ctrl+K)

File: templates/components/command_menu.html

<div x-data="{ open: false, search: '', items: [ { id: 1, label: 'Go to Dashboard', url: '/dashboard', icon: 'home' }, { id: 2, label: 'Settings', url: '/settings', icon: 'settings' } ], get filteredItems() { if (this.search === '') return this.items; return this.items.filter(i => i.label.toLowerCase().includes(this.search.toLowerCase())); } }"
    @keydown.window.prevent.cmd.k="open = !open" @keydown.window.prevent.ctrl.k="open = !open" @keydown.escape.window="open = false" style="display: none;" x-show="open" class="relative z-[100]">
    <div x-show="open" x-transition.opacity @click="open = false" class="fixed inset-0 bg-black/50 backdrop-blur-sm"></div>
    <div x-show="open" x-transition:enter="transition ease-out duration-200" x-transition:enter-start="opacity-0 scale-95" x-transition:enter-end="opacity-100 scale-100" class="fixed inset-0 flex items-start justify-center pt-[20vh] px-4">
        <div class="w-full max-w-xl bg-white rounded-xl shadow-2xl border border-gray-200 overflow-hidden flex flex-col max-h-[60vh]">
            <div class="flex items-center px-4 border-b border-gray-100">
                <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                <input x-model="search" type="text" placeholder="Search..." class="w-full h-14 px-4 text-gray-900 placeholder:text-gray-400 focus:outline-none bg-transparent" autofocus>
                <span class="text-xs text-gray-400 border border-gray-200 rounded px-1.5 py-0.5">ESC</span>
            </div>
            <div class="overflow-y-auto p-2">
                <template x-for="(item, index) in filteredItems" :key="item.id">
                    <a :href="item.url" class="flex items-center gap-3 px-3 py-3 rounded-lg hover:bg-gray-100 cursor-pointer group transition-colors" :class="{'bg-gray-100': index === 0}">
                        <span class="text-sm font-medium text-gray-700 group-hover:text-gray-900" x-text="item.label"></span>
                    </a>
                </template>
                <div x-show="filteredItems.length === 0" class="px-4 py-8 text-center text-sm text-gray-500">No results found.</div>
            </div>
        </div>
    </div>
</div>
