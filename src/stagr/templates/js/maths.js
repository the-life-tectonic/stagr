function number_sorter(a,b)
{
return a - b;
}

function prime(max) 
{
	var primes=[];
	if(max>1)
	{
		primes=[2];
		var n=3;
		while(n<=max)
		{
			var prime=true;
			for( var i in primes )
			{
				p=primes[i];
				if(n%p==0)
				{
					prime=false;
					break;
				}
			}
			if(prime)
			{
				primes.push(n);
			}
			n=n+2;
		}
	}
	return primes
}
			

function prime_factor(n,primes)
{
	if(n==1) { return []; }
	var fac=[];
	if(primes==undefined)
	{
		primes=prime(Math.sqrt(n));
	}

	for( var i in primes )
	{
		var p=primes[i];
		if(n%p==0)
		{
			fac=prime_factor( Math.floor(n/p) );
			fac.push(p);
			break;
		}
	}
	if(fac.length==0)
	{
		fac.push(n);
	}
	fac.sort(number_sorter);
	return fac;
}

function factors(n)
{
	var max=Math.sqrt(n)
	var factors=[1,n]
	for(var i=2; i<=max; i++)
	{
		if( n%i==0 )
		{
			factors.push(i);
			factors.push(n/i);
		}
	}
	factors.sort(number_sorter);
	return factors;
}

function rect(n)
{
	var f=factors(n);
	var a=f[Math.floor(f.length/2)];
	var r=[a,n/a];
	r.sort(number_sorter);
	return r;
}



