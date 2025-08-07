#!/usr/bin/env python3
"""
Script to create placeholder blog posts and categories for the portfolio website.
This script should be run after the database is set up and migrations are applied.
"""

import sys
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models import Category, Post, User
from app.schemas import CategoryCreate, PostCreate


def create_categories(db: Session):
    """Create blog post categories"""
    categories_data = [
        {"name": "Web Development", "slug": "web-development"},
        {"name": "React", "slug": "react"},
        {"name": "TypeScript", "slug": "typescript"},
        {"name": "Accessibility", "slug": "accessibility"},
        {"name": "DevOps", "slug": "devops"},
        {"name": "Technology", "slug": "technology"},
    ]

    categories = {}
    for cat_data in categories_data:
        # Check if category already exists
        existing = db.query(Category).filter(Category.slug == cat_data["slug"]).first()
        if existing:
            categories[cat_data["slug"]] = existing
            print(f"Category '{cat_data['name']}' already exists")
            continue

        category = Category(name=cat_data["name"], slug=cat_data["slug"])
        db.add(category)
        db.commit()
        db.refresh(category)
        categories[cat_data["slug"]] = category
        print(f"Created category: {cat_data['name']}")

    return categories


def create_blog_posts(db: Session, categories: dict, admin_user: User):
    """Create placeholder blog posts"""

    # Get the first admin user if no specific user is provided
    if not admin_user:
        admin_user = db.query(User).filter(User.is_admin == True).first()
        if not admin_user:
            print("No admin user found. Please create an admin user first.")
            return

    posts_data = [
        {
            "title": "Building Modern Web Applications with React and TypeScript",
            "slug": "building-modern-web-applications-react-typescript",
            "excerpt": "Explore the benefits of using TypeScript with React for building scalable, maintainable web applications. Learn best practices, common patterns, and how to avoid common pitfalls in modern web development.",
            "content": """
<h2>Introduction</h2>
<p>In today's fast-paced web development landscape, building applications that are both scalable and maintainable is crucial. React and TypeScript have emerged as a powerful combination that addresses these needs effectively.</p>

<h2>Why TypeScript with React?</h2>
<p>TypeScript provides static type checking that helps catch errors at compile time rather than runtime. When combined with React, it offers several benefits:</p>
<ul>
<li><strong>Better IDE Support:</strong> Enhanced autocomplete and IntelliSense</li>
<li><strong>Early Error Detection:</strong> Catch bugs before they reach production</li>
<li><strong>Improved Refactoring:</strong> Safe refactoring with confidence</li>
<li><strong>Better Documentation:</strong> Types serve as living documentation</li>
</ul>

<h2>Setting Up a React TypeScript Project</h2>
<p>Getting started with React and TypeScript is straightforward:</p>
<pre><code>npx create-react-app my-app --template typescript
# or with Vite
npm create vite@latest my-app -- --template react-ts</code></pre>

<h2>Best Practices</h2>
<p>Here are some key best practices when working with React and TypeScript:</p>
<ul>
<li>Define proper interfaces for your component props</li>
<li>Use generic types for reusable components</li>
<li>Leverage TypeScript's utility types</li>
<li>Implement proper error boundaries</li>
</ul>

<h2>Common Patterns</h2>
<p>Some common patterns that work well with React and TypeScript include:</p>
<ul>
<li>Custom hooks with proper typing</li>
<li>Context providers with typed values</li>
<li>Event handlers with proper event types</li>
<li>API calls with typed responses</li>
</ul>

<h2>Conclusion</h2>
<p>React and TypeScript together provide a robust foundation for building modern web applications. The combination offers the flexibility of React with the safety and developer experience of TypeScript, making it an excellent choice for both small and large-scale projects.</p>
            """,
            "read_time": "5 min read",
            "category_slug": "web-development",
            "published_at": datetime.utcnow() - timedelta(days=5),
        },
        {
            "title": "Optimizing React Performance: Best Practices and Tools",
            "slug": "optimizing-react-performance-best-practices-tools",
            "excerpt": "Learn how to identify and fix performance bottlenecks in your React applications using modern tools and techniques. Discover strategies for faster rendering and better user experience.",
            "content": """
<h2>Performance Matters</h2>
<p>In today's competitive web landscape, performance is not just a nice-to-have—it's essential. Users expect fast, responsive applications, and search engines favor faster sites.</p>

<h2>Identifying Performance Issues</h2>
<p>Before optimizing, you need to identify where the bottlenecks are:</p>
<ul>
<li><strong>React DevTools Profiler:</strong> Built-in tool for measuring render times</li>
<li><strong>Chrome DevTools:</strong> Performance tab for detailed analysis</li>
<li><strong>Lighthouse:</strong> Comprehensive performance auditing</li>
<li><strong>WebPageTest:</strong> Real-world performance testing</li>
</ul>

<h2>Common Performance Issues</h2>
<p>Some common performance issues in React applications include:</p>
<ul>
<li>Unnecessary re-renders</li>
<li>Large bundle sizes</li>
<li>Inefficient state management</li>
<li>Memory leaks</li>
<li>Blocking operations on the main thread</li>
</ul>

<h2>Optimization Techniques</h2>
<p>Here are proven techniques to improve React performance:</p>

<h3>1. Memoization</h3>
<p>Use React.memo, useMemo, and useCallback to prevent unnecessary re-renders:</p>
<pre><code>const MemoizedComponent = React.memo(({ data }) => {
  return <div>{data}</div>
});</code></pre>

<h3>2. Code Splitting</h3>
<p>Split your code into smaller chunks that can be loaded on demand:</p>
<pre><code>const LazyComponent = React.lazy(() => import('./LazyComponent'));</code></pre>

<h3>3. Virtual Scrolling</h3>
<p>For large lists, implement virtual scrolling to only render visible items.</p>

<h2>Tools and Libraries</h2>
<p>Several tools can help with React performance optimization:</p>
<ul>
<li><strong>React DevTools:</strong> Built-in profiling</li>
<li><strong>Why Did You Render:</strong> Identify unnecessary re-renders</li>
<li><strong>Bundle Analyzer:</strong> Analyze bundle size</li>
<li><strong>React Query:</strong> Efficient data fetching and caching</li>
</ul>

<h2>Conclusion</h2>
<p>Performance optimization is an ongoing process. Start by measuring, identify bottlenecks, implement optimizations, and measure again. The key is to make data-driven decisions and focus on the most impactful improvements.</p>
            """,
            "read_time": "6 min read",
            "category_slug": "react",
            "published_at": datetime.utcnow() - timedelta(days=8),
        },
        {
            "title": "TypeScript vs JavaScript: When to Use Each",
            "slug": "typescript-vs-javascript-when-to-use-each",
            "excerpt": "A comprehensive comparison of TypeScript and JavaScript, helping you decide which to use for your next project. Understand the trade-offs and benefits of each approach.",
            "content": """
<h2>The JavaScript Landscape</h2>
<p>JavaScript has evolved significantly since its creation in 1995. From a simple scripting language to a powerful, full-featured programming language, it now powers everything from web applications to server-side code.</p>

<h2>What is TypeScript?</h2>
<p>TypeScript is a superset of JavaScript that adds static type checking. It compiles down to JavaScript and provides additional tooling and safety features.</p>

<h2>Key Differences</h2>
<p>Let's explore the main differences between TypeScript and JavaScript:</p>

<h3>Type Safety</h3>
<p>TypeScript provides compile-time type checking, while JavaScript is dynamically typed:</p>
<pre><code>// JavaScript
function add(a, b) {
  return a + b;
}

// TypeScript
function add(a: number, b: number): number {
  return a + b;
}</code></pre>

<h3>Development Experience</h3>
<p>TypeScript offers better IDE support with enhanced autocomplete, error detection, and refactoring capabilities.</p>

<h3>Learning Curve</h3>
<p>JavaScript is easier to learn initially, while TypeScript requires understanding type systems and additional syntax.</p>

<h2>When to Use JavaScript</h2>
<p>JavaScript might be the better choice when:</p>
<ul>
<li>Building simple scripts or prototypes</li>
<li>Working with existing JavaScript codebases</li>
<li>Team members are new to programming</li>
<li>Quick iteration and experimentation is needed</li>
<li>Working with libraries that don't have TypeScript support</li>
</ul>

<h2>When to Use TypeScript</h2>
<p>TypeScript is ideal when:</p>
<ul>
<li>Building large, complex applications</li>
<li>Working in teams where code clarity is important</li>
<li>Building libraries or APIs that others will use</li>
<li>Long-term maintainability is a priority</li>
<li>Working with modern frameworks like React, Angular, or Vue</li>
</ul>

<h2>Migration Strategy</h2>
<p>If you're considering migrating from JavaScript to TypeScript:</p>
<ol>
<li>Start with a small, isolated module</li>
<li>Gradually add type annotations</li>
<li>Use the <code>any</code> type initially for complex scenarios</li>
<li>Enable strict mode gradually</li>
<li>Train your team on TypeScript concepts</li>
</ol>

<h2>Conclusion</h2>
<p>Both JavaScript and TypeScript have their place in modern web development. The choice depends on your project requirements, team expertise, and long-term goals. TypeScript is particularly valuable for larger projects where maintainability and team collaboration are important.</p>
            """,
            "read_time": "5 min read",
            "category_slug": "typescript",
            "published_at": datetime.utcnow() - timedelta(days=12),
        },
        {
            "title": "Building Accessible Web Applications",
            "slug": "building-accessible-web-applications",
            "excerpt": "Essential guidelines and techniques for creating web applications that work for everyone, including users with disabilities. Learn how to implement proper accessibility features.",
            "content": """
<h2>Why Accessibility Matters</h2>
<p>Web accessibility ensures that people with disabilities can perceive, understand, navigate, and interact with web applications. It's not just about compliance—it's about creating inclusive experiences for all users.</p>

<h2>Understanding Disabilities</h2>
<p>Different types of disabilities affect how users interact with web content:</p>
<ul>
<li><strong>Visual:</strong> Blindness, low vision, color blindness</li>
<li><strong>Auditory:</strong> Deafness, hard of hearing</li>
<li><strong>Motor:</strong> Limited mobility, tremors</li>
<li><strong>Cognitive:</strong> Learning disabilities, attention disorders</li>
</ul>

<h2>WCAG Guidelines</h2>
<p>The Web Content Accessibility Guidelines (WCAG) provide standards for web accessibility:</p>

<h3>Perceivable</h3>
<p>Information must be presentable to users in ways they can perceive:</p>
<ul>
<li>Provide text alternatives for non-text content</li>
<li>Create content that can be presented in different ways</li>
<li>Make it easier for users to see and hear content</li>
</ul>

<h3>Operable</h3>
<p>User interface components must be operable:</p>
<ul>
<li>Make all functionality available from a keyboard</li>
<li>Give users enough time to read and use content</li>
<li>Do not design content that could cause seizures</li>
<li>Provide ways to help users navigate and find content</li>
</ul>

<h3>Understandable</h3>
<p>Information and operation of user interface must be understandable:</p>
<ul>
<li>Make text readable and understandable</li>
<li>Make web pages appear and operate in predictable ways</li>
<li>Help users avoid and correct mistakes</li>
</ul>

<h3>Robust</h3>
<p>Content must be robust enough to be interpreted by a wide variety of user agents:</p>
<ul>
<li>Maximize compatibility with current and future user tools</li>
</ul>

<h2>Implementation Techniques</h2>
<p>Here are practical techniques for implementing accessibility:</p>

<h3>Semantic HTML</h3>
<p>Use proper HTML elements to convey meaning:</p>
<pre><code>&lt;button&gt;Submit&lt;/button&gt;  // Good
&lt;div onclick="submit()"&gt;Submit&lt;/div&gt;  // Bad</code></pre>

<h3>ARIA Labels</h3>
<p>Use ARIA attributes to provide additional context:</p>
<pre><code>&lt;button aria-label="Close dialog"&gt;×&lt;/button&gt;</code></pre>

<h3>Keyboard Navigation</h3>
<p>Ensure all interactive elements are keyboard accessible:</p>
<pre><code>// Handle keyboard events
const handleKeyDown = (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    handleClick();
  }
};</code></pre>

<h3>Color and Contrast</h3>
<p>Ensure sufficient color contrast and don't rely solely on color to convey information.</p>

<h2>Testing Accessibility</h2>
<p>Several tools can help test accessibility:</p>
<ul>
<li><strong>Screen Readers:</strong> NVDA, JAWS, VoiceOver</li>
<li><strong>Browser Extensions:</strong> axe DevTools, WAVE</li>
<li><strong>Automated Testing:</strong> Jest-axe, Cypress-axe</li>
<li><strong>Manual Testing:</strong> Keyboard navigation, color contrast checkers</li>
</ul>

<h2>Conclusion</h2>
<p>Accessibility should be considered from the beginning of your project, not as an afterthought. By following WCAG guidelines and implementing proper techniques, you can create web applications that work for everyone.</p>
            """,
            "read_time": "7 min read",
            "category_slug": "accessibility",
            "published_at": datetime.utcnow() - timedelta(days=15),
        },
        {
            "title": "Deploying to AWS: A Step-by-Step Guide",
            "slug": "deploying-to-aws-step-by-step-guide",
            "excerpt": "Complete walkthrough of deploying a React application to AWS using S3, CloudFront, and Route 53. Learn best practices for production deployments.",
            "content": """
<h2>Why AWS for Web Applications?</h2>
<p>Amazon Web Services (AWS) provides a comprehensive suite of services for deploying and hosting web applications. Its scalability, reliability, and cost-effectiveness make it an excellent choice for production deployments.</p>

<h2>Prerequisites</h2>
<p>Before starting, ensure you have:</p>
<ul>
<li>An AWS account</li>
<li>AWS CLI installed and configured</li>
<li>A React application ready for production</li>
<li>A domain name (optional but recommended)</li>
</ul>

<h2>Step 1: Build Your Application</h2>
<p>First, build your React application for production:</p>
<pre><code>npm run build</code></pre>
<p>This creates a <code>build</code> or <code>dist</code> folder with optimized static files.</p>

<h2>Step 2: Create an S3 Bucket</h2>
<p>S3 (Simple Storage Service) will host your static files:</p>
<ol>
<li>Go to the AWS S3 Console</li>
<li>Click "Create bucket"</li>
<li>Choose a unique bucket name</li>
<li>Select your preferred region</li>
<li>Configure bucket settings (keep defaults for now)</li>
<li>Set bucket permissions to allow public access</li>
</ol>

<h2>Step 3: Configure S3 for Static Website Hosting</h2>
<p>Enable static website hosting on your S3 bucket:</p>
<ol>
<li>Select your bucket in the S3 console</li>
<li>Go to the "Properties" tab</li>
<li>Scroll down to "Static website hosting"</li>
<li>Click "Edit" and enable it</li>
<li>Set the index document to <code>index.html</code></li>
<li>Set the error document to <code>index.html</code> (for SPA routing)</li>
<li>Save changes</li>
</ol>

<h2>Step 4: Upload Your Files</h2>
<p>Upload your built application files to the S3 bucket:</p>
<pre><code>aws s3 sync build/ s3://your-bucket-name --delete</code></pre>

<h2>Step 5: Set Up CloudFront Distribution</h2>
<p>CloudFront provides CDN capabilities and HTTPS:</p>
<ol>
<li>Go to the CloudFront console</li>
<li>Click "Create Distribution"</li>
<li>Set the origin domain to your S3 bucket's website endpoint</li>
<li>Configure viewer protocol policy to "Redirect HTTP to HTTPS"</li>
<li>Set the default root object to <code>index.html</li>
<li>Configure error pages to redirect 404s to <code>/index.html</code></li>
<li>Create the distribution</li>
</ol>

<h2>Step 6: Configure Custom Domain (Optional)</h2>
<p>If you have a domain name, you can set it up with Route 53:</p>
<ol>
<li>Register your domain with Route 53 or transfer it</li>
<li>Create a hosted zone for your domain</li>
<li>Request an SSL certificate through AWS Certificate Manager</li>
<li>Add an alternate domain name to your CloudFront distribution</li>
<li>Create an A record in Route 53 pointing to your CloudFront distribution</li>
</ol>

<h2>Step 7: Set Up CI/CD Pipeline</h2>
<p>Automate your deployments using GitHub Actions or AWS CodePipeline:</p>
<pre><code>name: Deploy to AWS
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm install
      - run: npm run build
      - run: aws s3 sync build/ s3://your-bucket-name --delete
      - run: aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"</code></pre>

<h2>Best Practices</h2>
<p>Follow these best practices for production deployments:</p>
<ul>
<li>Use environment variables for configuration</li>
<li>Implement proper error monitoring</li>
<li>Set up logging and analytics</li>
<li>Configure backup strategies</li>
<li>Monitor costs and usage</li>
<li>Implement security best practices</li>
</ul>

<h2>Monitoring and Maintenance</h2>
<p>After deployment, monitor your application:</p>
<ul>
<li>Set up CloudWatch alarms</li>
<li>Monitor CloudFront metrics</li>
<li>Check S3 access logs</li>
<li>Monitor costs and usage</li>
<li>Regular security updates</li>
</ul>

<h2>Conclusion</h2>
<p>AWS provides a robust platform for hosting web applications. By following this guide and implementing best practices, you can create a scalable, reliable, and cost-effective deployment solution.</p>
            """,
            "read_time": "8 min read",
            "category_slug": "devops",
            "published_at": datetime.utcnow() - timedelta(days=20),
        },
        {
            "title": "State Management in React: Context vs Redux",
            "slug": "state-management-react-context-redux",
            "excerpt": "Comparing different state management solutions in React and when to use each approach. Understand the trade-offs between Context API and Redux.",
            "content": """
<h2>The State Management Challenge</h2>
<p>As React applications grow in complexity, managing state becomes increasingly challenging. Choosing the right state management solution is crucial for maintainability and performance.</p>

<h2>React Context API</h2>
<p>The Context API is React's built-in solution for sharing state across components without prop drilling.</p>

<h3>Advantages</h3>
<ul>
<li>Built into React - no additional dependencies</li>
<li>Simple to set up and use</li>
<li>Great for small to medium applications</li>
<li>Perfect for theme, authentication, and language preferences</li>
</ul>

<h3>Disadvantages</h3>
<ul>
<li>Can cause unnecessary re-renders</li>
<li>No built-in performance optimizations</li>
<li>Limited debugging tools</li>
<li>Can become complex with multiple contexts</li>
</ul>

<h3>Example Implementation</h3>
<pre><code>// Create context
const ThemeContext = React.createContext();

// Provider component
const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');
  
  return (
    &lt;ThemeContext.Provider value={{ theme, setTheme }}&gt;
      {children}
    &lt;/ThemeContext.Provider&gt;
  );
};

// Consumer component
const ThemedButton = () => {
  const { theme, setTheme } = useContext(ThemeContext);
  
  return (
    &lt;button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}&gt;
      Toggle Theme
    &lt;/button&gt;
  );
};</code></pre>

<h2>Redux</h2>
<p>Redux is a predictable state container for JavaScript applications, particularly popular in the React ecosystem.</p>

<h3>Advantages</h3>
<ul>
<li>Predictable state updates</li>
<li>Excellent debugging with Redux DevTools</li>
<li>Great for large applications</li>
<li>Strong ecosystem and community</li>
<li>Time-travel debugging</li>
<li>Middleware support</li>
</ul>

<h3>Disadvantages</h3>
<ul>
<li>Additional bundle size</li>
<li>More boilerplate code</li>
<li>Steeper learning curve</li>
<li>Can be overkill for simple applications</li>
</ul>

<h3>Example Implementation</h3>
<pre><code>// Action
const toggleTheme = () => ({
  type: 'TOGGLE_THEME'
});

// Reducer
const themeReducer = (state = 'light', action) => {
  switch (action.type) {
    case 'TOGGLE_THEME':
      return state === 'light' ? 'dark' : 'light';
    default:
      return state;
  }
};

// Component
const ThemedButton = () => {
  const theme = useSelector(state => state.theme);
  const dispatch = useDispatch();
  
  return (
    &lt;button onClick={() => dispatch(toggleTheme())}&gt;
      Toggle Theme
    &lt;/button&gt;
  );
};</code></pre>

<h2>When to Use Context API</h2>
<p>Use Context API when:</p>
<ul>
<li>Building small to medium applications</li>
<li>Managing simple state like themes, authentication, or language</li>
<li>Want to avoid additional dependencies</li>
<li>Need a quick solution for prop drilling</li>
<li>Working with React's built-in features</li>
</ul>

<h2>When to Use Redux</h2>
<p>Use Redux when:</p>
<ul>
<li>Building large, complex applications</li>
<li>Need advanced debugging capabilities</li>
<li>Require middleware for side effects</li>
<li>Want predictable state updates</li>
<li>Need time-travel debugging</li>
<li>Working with teams that need clear state management patterns</li>
</ul>

<h2>Alternative Solutions</h2>
<p>Other state management solutions to consider:</p>

<h3>Zustand</h3>
<p>A small, fast, and scalable state management solution with minimal boilerplate.</p>

<h3>Recoil</h3>
<p>Facebook's experimental state management library with atomic state updates.</p>

<h3>Jotai</h3>
<p>Atomic state management library with React hooks.</p>

<h3>XState</h3>
<p>State machine library for managing complex state logic.</p>

<h2>Performance Considerations</h2>
<p>Consider these performance aspects:</p>
<ul>
<li>Context API can cause unnecessary re-renders</li>
<li>Redux provides better performance with large state trees</li>
<li>Use React.memo and useMemo for optimization</li>
<li>Consider code splitting for large applications</li>
</ul>

<h2>Migration Strategies</h2>
<p>If you need to migrate between solutions:</p>
<ol>
<li>Start with Context API for simple state</li>
<li>Migrate to Redux when complexity increases</li>
<li>Use both - Context for local state, Redux for global state</li>
<li>Consider modern alternatives like Zustand for simpler needs</li>
</ol>

<h2>Conclusion</h2>
<p>Both Context API and Redux have their place in React applications. The choice depends on your application's complexity, team size, and specific requirements. Start simple with Context API and migrate to Redux when needed.</p>
            """,
            "read_time": "6 min read",
            "category_slug": "react",
            "published_at": datetime.utcnow() - timedelta(days=25),
        },
    ]

    for post_data in posts_data:
        # Check if post already exists
        existing = db.query(Post).filter(Post.slug == post_data["slug"]).first()
        if existing:
            print(f"Post '{post_data['title']}' already exists")
            continue

        # Get category
        category = categories.get(post_data["category_slug"])
        if not category:
            print(
                f"Category '{post_data['category_slug']}' not found for post '{post_data['title']}'"
            )
            continue

        # Create post
        post = Post(
            title=post_data["title"],
            slug=post_data["slug"],
            content=post_data["content"].strip(),
            excerpt=post_data["excerpt"],
            read_time=post_data["read_time"],
            category_id=category.id,
            author_id=admin_user.id,
            published_at=post_data["published_at"],
        )

        db.add(post)
        db.commit()
        db.refresh(post)
        print(f"Created post: {post_data['title']}")


def main():
    """Main function to create categories and blog posts"""
    db = SessionLocal()

    try:
        print("Creating categories...")
        categories = create_categories(db)

        print("\nCreating blog posts...")
        create_blog_posts(db, categories, None)  # Will find admin user automatically

        print("\nBlog setup completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
